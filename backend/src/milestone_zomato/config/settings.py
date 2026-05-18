"""Application settings: dataset identity, LLM provider, secrets.

Values load from environment variables and optional ``.env`` (see ``.env.example``).
Phase 0 does not require API keys; Phase 3 will consume ``openai_api_key``.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from the environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    hf_dataset_id: str = Field(
        default="ManikaSaini/zomato-restaurant-recommendation",
        validation_alias=AliasChoices("ZOMATO_HF_DATASET", "HF_DATASET"),
        description="Hugging Face dataset repo id for restaurant rows.",
    )
    hf_dataset_revision: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("ZOMATO_HF_DATASET_REVISION", "HF_DATASET_REVISION"),
        description="Optional dataset revision (git commit) for repeatable ingestion.",
    )
    llm_provider: str = Field(
        default="openai",
        validation_alias=AliasChoices("ZOMATO_LLM_PROVIDER", "LLM_PROVIDER"),
        description="LLM vendor identifier (Phase 3).",
    )
    llm_model: str = Field(
        default="gpt-4o-mini",
        validation_alias=AliasChoices("ZOMATO_LLM_MODEL", "LLM_MODEL"),
        description="Model name passed to the provider API (Phase 3).",
    )
    openai_api_key: Optional[SecretStr] = Field(
        default=None,
        description="API key for OpenAI-compatible providers; optional until Phase 3.",
    )
    groq_api_key: Optional[SecretStr] = Field(
        default=None,
        description="API key for Groq; used in Phase 4 for fast summaries.",
    )
    restaurant_cache_path: str = Field(
        default="data/cache/restaurants.parquet",
        validation_alias=AliasChoices(
            "ZOMATO_RESTAURANT_CACHE_PATH",
            "RESTAURANT_CACHE_PATH",
        ),
        description="Parquet file written by Phase 1 ingest; read by list_restaurants().",
    )
    filter_top_k: int = Field(
        default=50,
        ge=1,
        le=500,
        validation_alias=AliasChoices("ZOMATO_FILTER_TOP_K", "FILTER_TOP_K"),
        description="Max candidates passed toward the LLM after deterministic filtering (Phase 2).",
    )


@lru_cache
def get_settings() -> Settings:
    """Return process-wide settings (cached)."""
    return Settings()
