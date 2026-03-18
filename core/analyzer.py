import json
import re

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from core.prompts import get_analysis_prompt
from models.schemas import ScriptAnalysis
from config.settings import settings


def _extract_json(raw: str) -> dict:
    """
    Robustly extract a JSON object from a raw LLM string response.
    Handles cases where the model wraps output in markdown code fences.
    """
    clean = re.sub(r"```(?:json)?", "", raw).replace("```", "").strip()

    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", clean, re.DOTALL)
    if match:
        return json.loads(match.group())

    raise ValueError(f"Could not extract valid JSON from model response:\n{raw[:500]}")


def build_analyzer_chain():
    """
    Builds and returns the LangChain analysis chain.
    Chain: PromptTemplate → ChatGoogleGenerativeAI → StrOutputParser
    """
    llm = ChatGoogleGenerativeAI(
        model=settings.model_name,
        temperature=settings.temperature,
        google_api_key=settings.google_api_key,
    )
    prompt = get_analysis_prompt()
    chain = prompt | llm | StrOutputParser()
    return chain


def analyze_script(script_text: str) -> ScriptAnalysis:
    """
    Run the full analysis pipeline on a script string.

    Args:
        script_text: Raw script content pasted by the user.

    Returns:
        ScriptAnalysis: A fully validated Pydantic model with all analysis fields.

    Raises:
        ValueError: If the LLM response cannot be parsed into the expected schema.
    """
    chain = build_analyzer_chain()
    raw_response = chain.invoke({"script": script_text})
    data = _extract_json(raw_response)
    return ScriptAnalysis(**data)
