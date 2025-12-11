"""Structured schema for UserSummaryAnalystAgent outputs."""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class TagMetric(BaseModel):
    tag: Optional[str] = None
    count: Optional[int] = Field(default=None, ge=0)
    accuracy: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    mean_rt_sec: Optional[float] = Field(default=None, ge=0.0)
    ability: Optional[float] = None
    dept_ability: Optional[float] = None


class MetricBundle(BaseModel):
    avg_response_time_sec: Optional[float] = Field(default=None, ge=0.0)
    by_tag: List[TagMetric] = Field(default_factory=list)


class InsightItem(BaseModel):
    summary: str
    tags: List[str]
    evidence: str
    metrics: MetricBundle


class LearningTrendMetrics(BaseModel):
    overall_theta_delta: Optional[float] = None
    trend: Literal["improving", "declining", "mixed", "unclear"]


class LearningTrend(BaseModel):
    summary: str
    trend: Literal["improving", "declining", "mixed", "unclear"]
    trend_metrics: LearningTrendMetrics


class FocusTopic(BaseModel):
    topic: str
    why: str
    tags: List[str]
    evidence: str


class ScenarioHeadline(BaseModel):
    scenario_id: Optional[int] = None
    scenario_name: Optional[str] = None
    accuracy: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    avg_response_time_seconds: Optional[float] = Field(default=None, ge=0.0)
    prompt_count: Optional[int] = Field(default=None, ge=0)
    tags: List[str] = Field(default_factory=list)


class PromptTypeMetrics(BaseModel):
    accuracy: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    avg_response_time_seconds: Optional[float] = Field(default=None, ge=0.0)
    trial_count: Optional[int] = Field(default=None, ge=0)


class PromptTypeSummary(BaseModel):
    single_answer: PromptTypeMetrics
    multi_choice: PromptTypeMetrics
    difference_in_accuracy: Optional[float] = None
    commentary: Optional[str] = None


class UserSummaryAnalysis(BaseModel):
    user_id: int
    username: Optional[str] = None
    department: Optional[str] = None
    user_summary: str
    scenario_headlines: List[ScenarioHeadline]
    strengths: List[InsightItem]
    weaknesses: List[InsightItem]
    learning_over_time: List[LearningTrend]
    focus_topics: List[FocusTopic]
    prompt_type_accuracy: Optional[PromptTypeSummary] = None
