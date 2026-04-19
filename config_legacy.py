"""
config_legacy.py — DEPRECATED.

This file is kept only so that `from config import Config` still resolves.
All active configuration now lives in config/settings.py.

There is NO Ollama / local-LLM configuration here anymore.
"""

# Re-export Config for any remaining import sites
from config.settings import Config  # noqa: F401
