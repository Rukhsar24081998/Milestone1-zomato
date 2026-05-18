"""Groq-powered summary blurb generation for Phase 4."""

from __future__ import annotations

import logging
import os
from typing import List

from groq import Groq

from milestone_zomato.config.settings import get_settings
from milestone_zomato_api.dto import PresentationResult

logger = logging.getLogger(__name__)


def generate_summary_blurb(results: List[PresentationResult]) -> str:
    """Generate a catchy, concise 2-sentence summary of the recommendations using Groq."""
    if not results:
        return "We couldn't find any restaurants matching those exact preferences."

    settings = get_settings()
    api_key = settings.groq_api_key.get_secret_value() if settings.groq_api_key else os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        logger.warning("GROQ_API_KEY not set. Skipping summary blurb generation.")
        return "Here are your top restaurant recommendations!"

    try:
        client = Groq(api_key=api_key)
        
        # Build prompt
        restaurant_names = ", ".join([r.name for r in results])
        prompt = f"""You are an enthusiastic food blogger. 
The user was just recommended these top restaurants: {restaurant_names}.
Write a fun, punchy, 2-sentence summary to hype up these choices. Do not list them out individually, just give a high-level hype summary."""

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful and enthusiastic foodie assistant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=settings.llm_model,
            temperature=0.7,
            max_tokens=100,
        )

        blurb = chat_completion.choices[0].message.content
        return blurb.strip() if blurb else "Enjoy these top picks!"
        
    except Exception as e:
        logger.error(f"Groq API call failed: {e}")
        return "Here are your top restaurant recommendations!"
