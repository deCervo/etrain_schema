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


class UserInformation(BaseModel):
    """Basic user information for report context."""

    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    department: Optional[str] = None


class UserSummaryReport(BaseModel):
    user: UserInformation
    user_summary: str
    strengths: List[InsightItem]
    weaknesses: List[InsightItem]
    learning_over_time: List[LearningTrend]
    focus_topics: List[FocusTopic]
    prompt_type_accuracy: PromptTypeComparison
