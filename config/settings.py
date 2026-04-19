import os
from dotenv import load_dotenv

# Load .env from the project root
load_dotenv()

# ---------------------------------------------------------------------------
# OpenRouter — the ONLY LLM backend supported by this project.
# ---------------------------------------------------------------------------
OPENROUTER_API_KEY: str | None = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
# "openrouter/auto" routes to the best currently-available free model automatically.
OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "openrouter/auto")

if not OPENROUTER_API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY is not set. "
        "Please create an account at https://openrouter.ai, "
        "generate an API key, and add it to your .env file:\n\n"
        "  OPENROUTER_API_KEY=sk-or-...\n"
    )

# ---------------------------------------------------------------------------
# Scraper settings (unchanged)
# ---------------------------------------------------------------------------
class Config:
    SCRAPER_USER_AGENT: str = os.getenv(
        "SCRAPER_USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    )
    SCRAPER_TIMEOUT: int = int(os.getenv("SCRAPER_TIMEOUT", "15"))
    SCRAPER_ENABLE_SELENIUM: bool = os.getenv("SCRAPER_ENABLE_SELENIUM", "true").lower() in (
        "true", "1", "t", "yes"
    )

    @classmethod
    def validate(cls) -> None:
        pass  # Scraper keys are all optional

Config.validate()
