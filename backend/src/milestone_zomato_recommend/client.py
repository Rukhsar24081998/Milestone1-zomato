"""Groq client wrapper with retries and structured output."""

from __future__ import annotations

import json
import os
from typing import List

from groq import Groq
from pydantic import BaseModel, ValidationError
from tenacity import retry, stop_after_attempt, wait_exponential

from milestone_zomato.config.settings import get_settings
from milestone_zomato.models.recommendation import Recommendation


class LLMRecommendationResponse(BaseModel):
    """Structured response required from the LLM."""

    recommendations: List[Recommendation]
    summary_blurb: str


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=20))
def call_llm(system_prompt: str, user_prompt: str) -> LLMRecommendationResponse:
    """Call the LLM with prompts, requesting a structured response."""
    settings = get_settings()

    # Use Groq
    api_key = settings.groq_api_key.get_secret_value() if settings.groq_api_key else os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set.")

    client = Groq(api_key=api_key)

    # Append JSON schema instruction to the prompt
    json_instruction = """
You MUST return ONLY a valid JSON object matching this schema:
{
  "recommendations": [
    {
      "restaurant_id": "string",
      "rank": 1,
      "explanation": "string"
    }
  ],
  "summary_blurb": "string"
}
"""
    completion = client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": system_prompt + json_instruction},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )

    content = completion.choices[0].message.content
    if not content:
        return LLMRecommendationResponse(recommendations=[], summary_blurb="No recommendations found.")

    try:
        parsed_data = json.loads(content)
        return LLMRecommendationResponse(**parsed_data)
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"Failed to parse LLM response: {e}\nContent: {content}")
        return LLMRecommendationResponse(recommendations=[], summary_blurb="Failed to parse recommendations.")
