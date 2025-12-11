"""Structured schema for UserSummaryWriterAgent outputs."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from .analysis import FocusTopic, InsightItem, LearningTrend


class PromptTypeComparison(BaseModel):
    """Narrative summary of single vs multi-choice performance."""

    summary: str
    single_answer_accuracy: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    multi_choice_accuracy: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    difference_in_accuracy: Optional[float] = None
    coaching_notes: List[str] = Field(default_factory=list)


class UserSummaryReport(BaseModel):
    user_summary: str
    strengths: List[InsightItem]
    weaknesses: List[InsightItem]
    learning_over_time: List[LearningTrend]
    focus_topics: List[FocusTopic]
    prompt_type_accuracy: PromptTypeComparison
