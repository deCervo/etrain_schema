"""Shared Pydantic schemas used across the eTRAIN platform."""

from __future__ import annotations

try:  # pragma: no cover - best effort metadata lookup
    from importlib.metadata import version as _pkg_version
except ImportError:  # Python <3.8 compatibility fallback
    def _pkg_version(_: str) -> str:  # type: ignore[override]
        return "0.0.0"

from .classroom_summary import ClassroomSummary
from .department.analysis import DepartmentAnalysis
from .department.graded import GradedIRTDepartmentAnalysis, GradedIRTDepartmentReport
from .department.report import DepartmentReport
from .learning_progress import DepartmentLearningProgress, LearningProgress
from .training_summary import TrainingSummary
from .user_summary.analysis import UserSummaryAnalysis
from .user_summary.graded import GradedIRTUserSummaryAnalysis, GradedIRTUserSummaryReport
from .user_summary.report import UserSummaryReport

try:
    __version__ = _pkg_version("etrain-schema")
except Exception:  # pragma: no cover - package not installed yet
    __version__ = "0.0.0"

__all__ = [
    "ClassroomSummary",
    "TrainingSummary",
    "DepartmentAnalysis",
    "DepartmentReport",
    "DepartmentLearningProgress",
    "LearningProgress",
    "GradedIRTDepartmentAnalysis",
    "GradedIRTDepartmentReport",
    "UserSummaryAnalysis",
    "UserSummaryReport",
    "GradedIRTUserSummaryAnalysis",
    "GradedIRTUserSummaryReport",
]
