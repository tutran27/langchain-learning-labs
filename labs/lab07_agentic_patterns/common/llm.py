"""LLM helper for Lab 07 agentic patterns."""

from __future__ import annotations

from typing import Any

from labs.lab01_foundation.llm_model import GroqLLMModel


def get_llm() -> Any:
    """Trả về ChatGroq LLM instance."""
    return GroqLLMModel().groq_chat()
