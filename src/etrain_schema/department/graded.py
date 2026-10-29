"""Structured department-report schemas for the graded-IRT analytics contract."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from etrain_schema.learning_progress import DepartmentLearningProgress

from .analysis import DepartmentAnalysis
from .report import DepartmentReport


class DepartmentReportSnapshot(BaseModel):
    """Backend-captured report scope; no direct identity fields."""

    active_only: bool
    captured_at: str
    user_count: int = Field(..., ge=0)


class GradedIRTDepartmentAnalysis(DepartmentAnalysis):
    analytics_contract_version: Literal["graded_irt_v1"]
    calibration_version: str
    learning_progress: DepartmentLearningProgress


class GradedIRTDepartmentReport(DepartmentReport):
    report_snapshot: Optional[DepartmentReportSnapshot] = None
    analytics_contract_version: Literal["graded_irt_v1"]
    calibration_version: str
    learning_progress: DepartmentLearningProgress
