"""Contract tests for graded-IRT shared schemas."""

import pytest

from etrain_schema import (
    DepartmentLearningProgress,
    GradedIRTUserSummaryReport,
    LearningProgress,
)


def learning_progress(*, classification: str = "improving") -> dict:
    return {
        "model": {
            "type": "graded_response_1pl",
            "calibration_version": "cal-1",
            "status": "ready",
        },
        "evidence": {
            "baseline_target": 10,
            "qualified_responses": 20,
            "total_scoreable_responses": 22,
            "skipped_responses": 2,
            "strength": "established",
        },
        "current": {
            "percentile": 61,
            "comparison_population": "Department peers",
        },
        "change_from_baseline": {
            "normalized_change": 0.3,
            "classification": classification,
            "probability": 0.82,
        },
    }


@pytest.mark.parametrize(
    "classification",
    ["improving", "declining", "holding_steady", "no_clear_change", "baseline_forming"],
)
def test_learning_progress_accepts_backend_classifications(classification):
    progress = LearningProgress.model_validate(
        learning_progress(classification=classification)
    )

    assert progress.change_from_baseline.classification == classification


def test_graded_user_report_validates_learning_progress():
    report = GradedIRTUserSummaryReport.model_validate(
        {
            "analytics_contract_version": "graded_irt_v1",
            "calibration_version": "cal-1",
            "readiness_status": "ready",
            "user": {"user_id": 42, "username": "officer"},
            "user_summary": "Current training summary.",
            "strengths": [],
            "weaknesses": [],
            "learning_over_time": [
                {
                    "summary": "Backend-classified progress.",
                    "learning_progress": learning_progress(),
                }
            ],
            "focus_topics": [],
            "prompt_type_accuracy": {
                "summary": "No material interaction-type gap.",
                "coaching_notes": [],
            },
        }
    )

    assert report.analytics_contract_version == "graded_irt_v1"


def test_graded_department_report_requires_privacy_safe_progress():
    with pytest.raises(ValueError):
        DepartmentLearningProgress.model_validate(
            {
                "calibration_version": "cal-1",
                "active_officer_count": 4,
                "officers_with_established_baselines": 4,
                "classification_counts": {},
                "evidence_strength_distribution": {},
                "response_coverage": {
                    "qualified_responses": 20,
                    "total_scoreable_responses": 20,
                    "skipped_responses": 0,
                },
                "tag_progress": [
                    {
                        "tag": "Constitutional Policing",
                        "officers_qualified": 4,
                        "classification_counts": {},
                        "evidence_strength_distribution": {},
                    }
                ],
            }
        )


def test_department_movement_counts_are_optional_and_survive_serialization():
    payload = {
        "calibration_version": "cal-1",
        "active_officer_count": 8,
        "officers_with_established_baselines": 8,
        "classification_counts": {"improving": 1, "no_clear_change": 7},
        "evidence_strength_distribution": {"established": 8},
        "response_coverage": {"qualified_responses": 100, "total_scoreable_responses": 120, "skipped_responses": 20},
    }
    assert DepartmentLearningProgress.model_validate(payload).movement_counts is None
    payload["movement_counts"] = {"improving": 1, "positive_movement": 5, "negative_movement": 1, "no_clear_change": 1}
    saved = DepartmentLearningProgress.model_validate(payload).model_dump()
    assert saved["movement_counts"]["positive_movement"] == 5
    assert saved["classification_counts"]["no_clear_change"] == 7
    payload["movement_counts"]["positive_movement"] = -1
    with pytest.raises(ValueError):
        DepartmentLearningProgress.model_validate(payload)


@pytest.mark.parametrize("usernames", [None, {}, {"improving": ["Officer_7", "alpha"], "declining": ["bravo"]}])
def test_department_classification_usernames_round_trip(usernames):
    payload = {
        "calibration_version": "cal-1",
        "active_officer_count": 8,
        "officers_with_established_baselines": 8,
        "classification_counts": {"improving": 2, "declining": 1},
        "evidence_strength_distribution": {"established": 8},
        "response_coverage": {"qualified_responses": 100, "total_scoreable_responses": 120, "skipped_responses": 20},
    }
    assert DepartmentLearningProgress.model_validate(payload).classification_usernames is None
    payload["classification_usernames"] = usernames
    saved = DepartmentLearningProgress.model_validate(payload).model_dump()
    if usernames is None:
        assert saved["classification_usernames"] is None
    else:
        assert saved["classification_usernames"] == {"improving": [], "declining": [], **usernames}
    payload["classification_usernames"] = {"improving": [{"first_name": "Not a username"}]}
    with pytest.raises(ValueError):
        DepartmentLearningProgress.model_validate(payload)
