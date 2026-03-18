from pydantic import BaseModel, Field
from typing import List, Optional


class EmotionalArc(BaseModel):
    opening: str = Field(description="Dominant emotion at the start of the script")
    middle: str = Field(description="Emotional shift or tension in the middle")
    closing: str = Field(description="Emotional state or feeling at the end")


class EmotionalAnalysis(BaseModel):
    dominant_emotions: List[str] = Field(description="Top 2-4 dominant emotions present in the script")
    arc: EmotionalArc = Field(description="How emotions evolve across the script's three acts")
    tone_summary: str = Field(description="One or two sentence summary of the overall emotional tone")


class EngagementFactor(BaseModel):
    name: str = Field(description="Name of the engagement factor, e.g. 'Opening Hook'")
    score: int = Field(description="Score from 1 to 10 for this factor")
    reasoning: str = Field(description="Short explanation of why this score was given")


class EngagementAnalysis(BaseModel):
    overall_score: int = Field(description="Overall engagement score from 1 to 10")
    factors: List[EngagementFactor] = Field(description="List of scored engagement factors")
    verdict: str = Field(description="One sentence verdict on the script's engagement potential")


class ImprovementSuggestion(BaseModel):
    area: str = Field(description="Storytelling area to improve, e.g. 'Pacing', 'Dialogue', 'Conflict'")
    suggestion: str = Field(description="Concrete suggestion for how to improve this area")


class CliffhangerMoment(BaseModel):
    moment: str = Field(description="The exact line or scene that acts as the cliffhanger or peak suspense")
    explanation: str = Field(description="Why this moment creates suspense or compels the audience forward")


class ScriptAnalysis(BaseModel):
    summary: str = Field(description="A 3-4 line story summary")
    emotional_analysis: EmotionalAnalysis
    engagement: EngagementAnalysis
    improvement_suggestions: List[ImprovementSuggestion] = Field(
        description="3-5 actionable improvement suggestions"
    )
    cliffhanger: Optional[CliffhangerMoment] = Field(
        default=None,
        description="The most suspenseful or cliffhanger moment in the script"
    )
