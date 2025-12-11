from __future__ import annotations

from typing import List, Optional, Union

from pydantic import BaseModel


class ChoiceOption(BaseModel):
    """Individual choice-level statistics."""

    choice_id: Optional[int]
    text: Optional[str]
    percent_selected: Optional[float]


ChoiceDetail = Union[List[ChoiceOption], ChoiceOption, None]


class ClassroomOverviewScenario(BaseModel):
    """Summary for a scenario listed inside the classroom overview."""

    id: Optional[int]
    name: Optional[str]
    accuracy: Optional[float]
    avg_response_time_seconds: Optional[float]
    number_of_prompts: Optional[int]
    unique_participants: Optional[int]


class ClassroomOverview(BaseModel):
    """Top-level classroom summary metadata."""

    session_name: Optional[str]
    date: Optional[str]
    participants: int
    overall_accuracy: Optional[float]
    avg_response_time_seconds: Optional[float]
    scenarios: Optional[List[ClassroomOverviewScenario]]


class ByTagSummary(BaseModel):
    """Aggregated performance information grouped by tag."""

    tag: Optional[str]
    accuracy: Optional[float]
    avg_response_time_seconds: Optional[float]
    total_questions: int
    total_correct: int
    number_of_prompts: int
    tag_summary: Optional[str]


class ScenarioDetail(BaseModel):
    """Scenario-level metrics exposed outside the overview block."""

    scenario_id: Optional[int]
    scenario_name: Optional[str]
    accuracy: Optional[float]
    avg_response_time_seconds: Optional[float]
    number_of_prompts: Optional[int]
    unique_participants: Optional[int]


class PromptHighlight(BaseModel):
    """A single prompt-level highlight or struggle."""

    prompt_id: Optional[int]
    prompt_text: Optional[str]
    scenario_name: Optional[str]
    avg_accuracy: Optional[float]
    attempts: int
    correct_answer: ChoiceDetail
    correct_answer_explanation: Optional[str]


class LowPerformingPrompt(PromptHighlight):
    """Additional detail for prompts where accuracy was low."""

    highest_chosen_incorrect_answer: Optional[ChoiceOption]


class FocusArea(BaseModel):
    """Coaching opportunity identified during the session."""

    tag: Optional[str]
    issue: str
    recommendation: str


class ClassroomSummary(BaseModel):
    """Full JSON structure returned by the ClassroomSummary agent."""

    classroom_overview: ClassroomOverview
    topics_summary: str
    scenarios: Optional[List[ScenarioDetail]]
    by_tag: List[ByTagSummary]
    highlights: List[PromptHighlight]
    low_performing_prompts: List[LowPerformingPrompt]
    focus_areas: List[FocusArea]


CLASSROOM_SUMMARY_JSON_SCHEMA = ClassroomSummary.model_json_schema()
