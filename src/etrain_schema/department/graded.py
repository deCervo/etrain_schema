"""Structured department-report schemas for the graded-IRT analytics contract."""

from __future__ import annotations

from typing import Literal

from etrain_schema.learning_progress import DepartmentLearningProgress

from .analysis import DepartmentAnalysis
from .report import DepartmentReport


class GradedIRTDepartmentAnalysis(DepartmentAnalysis):
    analytics_contract_version: Literal["graded_irt_v1"]
    calibration_version: str
    learning_progress: DepartmentLearningProgress


class GradedIRTDepartmentReport(DepartmentReport):
    analytics_contract_version: Literal["graded_irt_v1"]
    calibration_version: str
    learning_progress: DepartmentLearningProgress
