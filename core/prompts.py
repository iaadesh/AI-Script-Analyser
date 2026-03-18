from langchain_core.prompts import ChatPromptTemplate

# ---------------------------------------------------------------------------
# Few-shot example used to ground the model's output style and format
# ---------------------------------------------------------------------------

FEW_SHOT_EXAMPLE = """
EXAMPLE INPUT SCRIPT:
---
Title: One Last Call

Scene
Maya stands outside a hospital. Her phone rings. It's her estranged father.

Dialogue
Maya: Dad? It's 2 AM.
Father: I know. I just... I needed to hear your voice.
Maya: Are you okay?
Father: I will be. After tonight.
Maya: What happens tonight?
Father: (pause) Nothing. I love you, Maya.
---

EXAMPLE OUTPUT (JSON):
{{
  "summary": "Maya receives an unexpected late-night call from her estranged father, who is clearly hiding something. The conversation is warm on the surface but carries an undercurrent of dread. The cryptic sign-off leaves Maya — and the audience — deeply unsettled about what her father means by 'after tonight.'",

  "emotional_analysis": {{
    "dominant_emotions": ["Unease", "Longing", "Dread", "Love"],
    "arc": {{
      "opening": "Surprise and confusion — an unexpected call in the middle of the night.",
      "middle": "Warmth mixed with rising anxiety as the father's words feel loaded.",
      "closing": "Haunting dread — the audience is left with the feeling that something irreversible is about to happen."
    }},
    "tone_summary": "The script blends quiet tenderness with creeping dread. The emotional current runs deep beneath the surface of ordinary dialogue."
  }},

  "engagement": {{
    "overall_score": 8,
    "factors": [
      {{"name": "Opening Hook", "score": 9, "reasoning": "A 2 AM hospital call from an estranged parent is immediately intriguing."}},
      {{"name": "Character Conflict", "score": 7, "reasoning": "The estrangement is implied but not over-explained, creating intrigue."}},
      {{"name": "Tension", "score": 8, "reasoning": "Every line from the father hints at a secret, ratcheting up the stakes."}},
      {{"name": "Cliffhanger", "score": 9, "reasoning": "'After tonight' is a devastating, open-ended line that demands resolution."}}
    ],
    "verdict": "A tightly wound scene with exceptional emotional pull that will keep audiences hooked."
  }},

  "improvement_suggestions": [
    {{"area": "Setting", "suggestion": "Use the hospital backdrop more actively — a passing doctor, a PA announcement — to raise the stakes."}},
    {{"area": "Maya's Voice", "suggestion": "Give Maya one line that hints at the history between them, adding weight to her reaction."}},
    {{"area": "Pacing", "suggestion": "A brief silent pause notated in the script before the father's last line would amplify its impact."}},
    {{"area": "Ambiguity Control", "suggestion": "The cryptic ending is strong, but one more concrete detail from the father would balance mystery with clarity."}}
  ],

  "cliffhanger": {{
    "moment": "Father: 'I will be. After tonight.'",
    "explanation": "This line reframes the entire call. What seemed like a reconciliation becomes a possible goodbye, activating the audience's worst fears without confirming them — a masterclass in subtext."
  }}
}}
"""

# ---------------------------------------------------------------------------
# Main analysis prompt
# ---------------------------------------------------------------------------
ANALYSIS_SYSTEM_PROMPT = """You are an expert script analyst and story consultant with decades of experience \
evaluating short-form scripted content for film, television, and digital platforms. \
You specialize in understanding narrative structure, emotional resonance, and audience engagement.

Your role is to analyze a short script and return a precise, structured JSON analysis. \
You must be candid, specific, and actionable — not generic. \
Reference actual lines and moments from the script to support your analysis.

{few_shot_example}

Now analyze the script provided by the user using the EXACT same JSON structure shown above. \
Return ONLY valid JSON. No markdown, no code fences, no extra explanation. Just the JSON object."""

ANALYSIS_HUMAN_PROMPT = """Please analyze the following script:

---
{script}
---

Return your full structured analysis as a JSON object following the example format exactly."""


def get_analysis_prompt() -> ChatPromptTemplate:
    """Returns the ChatPromptTemplate for the full script analysis chain."""
    return ChatPromptTemplate.from_messages([
        ("system", ANALYSIS_SYSTEM_PROMPT.format(few_shot_example=FEW_SHOT_EXAMPLE)),
        ("human", ANALYSIS_HUMAN_PROMPT),
    ])
