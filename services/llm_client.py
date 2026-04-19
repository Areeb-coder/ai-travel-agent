"""
services/llm_client.py — OpenRouter-only LLM client.

This module is the single place in the codebase that makes LLM API calls.
All calls go to OpenRouter's /chat/completions endpoint (OpenAI-compatible).

There is NO support for Ollama, local models, or any other provider.
"""

import json
from typing import Dict, List, Optional

import requests

from config.settings import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_MODEL,
)


class LLMError(RuntimeError):
    """Raised when the OpenRouter call fails for any reason."""


def generate_completion(
    messages: List[Dict[str, str]],
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    timeout: int = 60,
    model: Optional[str] = None,
    **_ignored,  # absorb legacy keyword args gracefully
) -> str:
    """
    Call OpenRouter's /chat/completions endpoint.

    Args:
        messages:       List of {"role": "user"|"assistant", "content": str}.
        system_prompt:  Optional system-level instruction prepended to the conversation.
        temperature:    Sampling temperature (default 0.7).
        timeout:        HTTP request timeout in seconds (default 60).
        model:          Override the default model from .env.

    Returns:
        The assistant's reply as a plain string.

    Raises:
        LLMError: On any network, HTTP, or schema error.
    """
    url = f"{OPENROUTER_BASE_URL.rstrip('/')}/chat/completions"

    all_messages: List[Dict[str, str]] = []
    if system_prompt:
        all_messages.append({"role": "system", "content": system_prompt})
    all_messages.extend(messages)

    payload = {
        "model": model or OPENROUTER_MODEL,
        "messages": all_messages,
        "temperature": temperature,
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        # Recommended by OpenRouter for analytics / rate-limit attribution:
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "AI Travel Agent",
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
    except Exception as exc:
        raise LLMError(
            f"Failed to communicate with OpenRouter at {url}: {exc}"
        ) from exc

    if not resp.ok:
        raise LLMError(
            f"OpenRouter responded with status {resp.status_code}: {resp.text[:500]}"
        )

    try:
        data = resp.json()
    except Exception as exc:
        raise LLMError(
            f"Failed to parse OpenRouter JSON response: {resp.text[:500]}"
        ) from exc

    try:
        content: str = data["choices"][0]["message"]["content"]
    except Exception as exc:
        raise LLMError(f"Unexpected OpenRouter response schema: {data}") from exc

    return content


def generate_itinerary(system_prompt: str, user_prompt: str, **opts) -> dict:
    """
    Backwards-compatible helper: calls generate_completion and parses JSON.

    Strips ```json … ``` or ``` … ``` fences before parsing.
    """
    text = generate_completion(
        messages=[{"role": "user", "content": user_prompt}],
        system_prompt=system_prompt,
        **opts,
    )

    # Strip markdown code fences if the model wrapped its output
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise LLMError(
            f"OpenRouter did not return valid JSON. Raw output:\n{text}"
        ) from exc
