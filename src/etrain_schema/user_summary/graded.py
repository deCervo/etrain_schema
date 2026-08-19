"""Structured user-report schemas for the graded-IRT analytics contract."""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from etrain_schema.learning_progress import LearningProgress, LearningProgressStatus

from .analysis import FocusTopic, PromptTypeSummary, ScenarioHeadline
from .report import PromptTypeComparison, UserInformation


class GradedTagMetric(BaseModel):
    tag: Optional[str] = None
    count: Optional[int] = Field(default=None, ge=0)
    accuracy: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    mean_rt_sec: Optional[float] = Field(default=None, ge=0.0)
    learning_progress: Optional[LearningProgress] = None


class GradedMetricBundle(BaseModel):
    avg_response_time_sec: Optional[float] = Field(default=None, ge=0.0)
    by_tag: List[GradedTagMetric] = Field(default_factory=list)


class GradedInsightItem(BaseModel):
    summary: str
    tags: List[str]
    evidence: str
    metrics: GradedMetricBundle


class GradedLearningTrend(BaseModel):
    summary: str
    learning_progress: LearningProgress


class GradedIRTUserSummaryAnalysis(BaseModel):
    analytics_contract_version: Literal["graded_irt_v1"]
    calibration_version: str
    readiness_status: LearningProgressStatus
    user_id: int
    username: Optional[str] = None
    department: Optional[str] = None
    user_summary: str
    scenario_headlines: List[ScenarioHeadline]
    strengths: List[GradedInsightItem]
    weaknesses: List[GradedInsightItem]
    learning_over_time: List[GradedLearningTrend]
    focus_topics: List[FocusTopic]
    prompt_type_accuracy: Optional[PromptTypeSummary] = None


class GradedIRTUserSummaryReport(BaseModel):
    analytics_contract_version: Literal["graded_irt_v1"]
    calibration_version: str
    readiness_status: LearningProgressStatus
    user: UserInformation
    user_summary: str
    strengths: List[GradedInsightItem]
    weaknesses: List[GradedInsightItem]
    learning_over_time: List[GradedLearningTrend]
    focus_topics: List[FocusTopic]
    prompt_type_accuracy: PromptTypeComparison
