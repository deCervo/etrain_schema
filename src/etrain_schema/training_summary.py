from __future__ import annotations

from typing import List, Optional, Union

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    """Concrete example supporting a skill."""

    prompt_id: int
    prompt_text: str
    user_response: List[str]
    trial_accuracy: Union[float, str] = Field(
        ...,
        description='Numeric accuracy (0–1) or "Unknown".',
    )
    rationale: str


class Skill(BaseModel):
    """A skill demonstrated in the session."""

    name: str
    evidence: List[Evidence]


class AreaForImprovement(BaseModel):
    """A focus area with a concrete recommendation."""

    area: str
    recommendation: str


class TimelineHighlight(BaseModel):
    """A notable moment in the session timeline."""

    prompt_id: int
    highlight: str
    trial_accuracy: Union[float, str]


class SessionOverview(BaseModel):
    """Top-level information about the training session."""

    date: str
    overall_accuracy: str
    avg_response_time_seconds: Optional[float]
    tags: List[str]
    scenarios: List[str]


class TrainingSummary(BaseModel):
    """
    Full training summary for a single session.

    This is the schema the LLM should conform to when generating output.
    """

    session_overview: SessionOverview
    training_objectives: str
    skills: List[Skill]
    strengths: List[str]
    areas_for_improvement: List[AreaForImprovement]
    timeline_highlights: List[TimelineHighlight]


TRAINING_SUMMARY_JSON_SCHEMA = TrainingSummary.model_json_schema()
