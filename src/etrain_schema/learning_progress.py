"""Shared graded-IRT learning-progress contracts."""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


LearningProgressStatus = Literal["ready", "baseline_forming", "rebuilding", "stale"]
LearningClassification = Literal[
    "improving",
    "declining",
    "holding_steady",
    "no_clear_change",
    "baseline_forming",
]
EvidenceStrength = Literal["baseline_forming", "developing", "established"]


class LearningModelContext(BaseModel):
    type: Literal["graded_response_1pl"]
    calibration_version: str
    status: LearningProgressStatus


class LearningEvidence(BaseModel):
    baseline_target: int = Field(default=10, ge=1)
    qualified_responses: int = Field(..., ge=0)
    total_scoreable_responses: int = Field(..., ge=0)
    skipped_responses: int = Field(..., ge=0)
    strength: EvidenceStrength


class LearningCurrentComparison(BaseModel):
    percentile: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    comparison_population: Optional[str] = None


class LearningChangeFromBaseline(BaseModel):
    normalized_change: Optional[float] = None
    classification: LearningClassification
    probability: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class LearningProgress(BaseModel):
    model: LearningModelContext
    evidence: LearningEvidence
    current: LearningCurrentComparison
    change_from_baseline: LearningChangeFromBaseline


class ClassificationCounts(BaseModel):
    improving: int = Field(default=0, ge=0)
    declining: int = Field(default=0, ge=0)
    holding_steady: int = Field(default=0, ge=0)
    no_clear_change: int = Field(default=0, ge=0)
    baseline_forming: int = Field(default=0, ge=0)


class EvidenceStrengthCounts(BaseModel):
    baseline_forming: int = Field(default=0, ge=0)
    developing: int = Field(default=0, ge=0)
    established: int = Field(default=0, ge=0)


class ResponseCoverage(BaseModel):
    qualified_responses: int = Field(..., ge=0)
    total_scoreable_responses: int = Field(..., ge=0)
    skipped_responses: int = Field(..., ge=0)
    qualified_rate: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    skipped_rate: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class AggregateTagProgress(BaseModel):
    tag: str
    officers_qualified: int = Field(..., ge=5)
    median_normalized_change: Optional[float] = None
    classification_counts: ClassificationCounts
    evidence_strength_distribution: EvidenceStrengthCounts


class DepartmentLearningProgress(BaseModel):
    calibration_version: str
    active_officer_count: int = Field(..., ge=0)
    officers_with_established_baselines: int = Field(..., ge=0)
    classification_counts: ClassificationCounts
    evidence_strength_distribution: EvidenceStrengthCounts
    median_normalized_change: Optional[float] = None
    response_coverage: ResponseCoverage
    comparison_percentile: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    comparison_population: Optional[str] = None
    tag_progress: List[AggregateTagProgress] = Field(default_factory=list)
    minimum_cohort_size: int = Field(default=5, ge=5)
