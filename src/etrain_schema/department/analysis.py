"""Structured schema for DepartmentAnalystAgent outputs."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class TagPerformance(BaseModel):
    tag: str
    accuracy_pct: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    accuracy_stddev: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    total_prompts: int = Field(..., ge=0)
    total_choices: int = Field(..., ge=0)
    officers_covered: int = Field(..., ge=0)
    avg_response_time_seconds: Optional[float] = Field(default=None, ge=0.0)


class ScenarioSummary(BaseModel):
    scenario_id: int
    name: str
    tags: List[str]
    difficulty: Optional[float] = Field(default=None, ge=-10.0, le=10.0)
    accuracy_pct: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    accuracy_stddev: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    num_prompts: int = Field(..., ge=0)
    num_sessions: int = Field(..., ge=0)
    avg_response_time_seconds: Optional[float] = Field(default=None, ge=0.0)
    insight: Optional[str] = None


class ClusterSummary(BaseModel):
    domain: str
    tags: List[str]
    avg_accuracy_pct: float = Field(..., ge=0.0, le=100.0)
    classification: str  # "Strength" or "Weakness"
    summary: str


class AccuracyBucket(BaseModel):
    accuracy_pct: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    prompt_count: int = Field(..., ge=0)


class TagInteraction(BaseModel):
    tag_a: str
    tag_b: str
    single_tag_a: AccuracyBucket
    single_tag_b: AccuracyBucket
    joint: AccuracyBucket
    delta_pct: Optional[float] = None
    interpretation: Optional[str] = None


class PromptTypeMetrics(BaseModel):
    accuracy_pct: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    avg_response_time_seconds: Optional[float] = Field(default=None, ge=0.0)


class UserPromptTypeComparison(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None
    single_answer_metrics: Optional[PromptTypeMetrics] = None
    multi_choice_metrics: Optional[PromptTypeMetrics] = None
    difference_in_accuracy_pct: Optional[float] = None


class DepartmentPromptTypeComparison(BaseModel):
    department_avg_difference_pct: Optional[float] = None
    users: List[UserPromptTypeComparison]


class DepartmentAnalysis(BaseModel):
    department_id: int
    department_name: str
    active_only: bool
    num_officers: int = Field(..., ge=0)
    num_sessions: int = Field(..., ge=0)
    num_prompts: int = Field(..., ge=0)
    overall_accuracy_pct: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    accuracy_stddev: Optional[float] = Field(default=None, ge=0.0)
    avg_response_time_seconds: Optional[float] = Field(default=None, ge=0.0)
    response_time_stddev: Optional[float] = Field(default=None, ge=0.0)

    strengths: List[TagPerformance]
    weaknesses: List[TagPerformance]

    low_scenarios: List[ScenarioSummary]
    high_scenarios: List[ScenarioSummary]

    clusters: List[ClusterSummary]
    tag_interactions: List[TagInteraction]
    prompt_type_comparison: Optional[DepartmentPromptTypeComparison] = None

    notes: Optional[str] = None
