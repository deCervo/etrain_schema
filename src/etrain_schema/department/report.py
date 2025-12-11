"""Structured schema for DepartmentWriterAgent outputs."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class TagItem(BaseModel):
    tag: str
    accuracy_pct: float = Field(..., ge=0.0, le=100.0)


class TrainingNeed(BaseModel):
    title: str
    description: str


class ScenarioInsight(BaseModel):
    scenario_id: Optional[int]
    scenario_name: str
    tags: List[str]
    accuracy_pct: float = Field(..., ge=0.0, le=100.0)
    what_to_fix: str


class DomainClusterReport(BaseModel):
    domain: str
    tags: List[str]
    avg_accuracy_pct: float = Field(..., ge=0.0, le=100.0)
    classification: str
    summary: str


class TagInteractionReport(BaseModel):
    tags: List[str]
    delta_pct: float
    interpretation: str


class ConceptReinforcementItem(BaseModel):
    concept: str
    explanation: str


class PromptTypeOutlierReport(BaseModel):
    username: str
    single_answer_accuracy_pct: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    multi_choice_accuracy_pct: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    delta_pct: float
    interpretation: str


class PromptTypeComparisonReport(BaseModel):
    average_difference_pct: float
    summary: str
    outliers: List[PromptTypeOutlierReport]


class DepartmentReport(BaseModel):
    quick_overview: str

    strengths: List[TagItem]
    weaknesses: List[TagItem]
    training_needs: List[TrainingNeed]

    scenario_insights: List[ScenarioInsight]

    domain_clusters: List[DomainClusterReport]

    tag_interactions: List[TagInteractionReport]

    prompt_type_comparison: PromptTypeComparisonReport

    concept_reinforcement: List[ConceptReinforcementItem]

    meta_pattern: str
