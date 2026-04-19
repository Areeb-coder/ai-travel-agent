"""
llm_client.py (project root) — thin shim for backwards compatibility.

All real logic lives in services/llm_client.py.
Importing from here re-exports the same symbols so that any legacy
code that did `from llm_client import generate_itinerary` still works.

There are NO Ollama / local-LLM references here.
"""

from services.llm_client import (  # noqa: F401  (re-export)
    LLMError,
    generate_completion,
    generate_itinerary,
)
