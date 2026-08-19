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
