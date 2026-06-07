"""
src/config.py
=============
Central configuration module for ResearchCrew.

Responsibilities:
  - Load all environment variables from .env
  - Expose typed constants used across the project
  - Validate that required API keys are present at startup
  - Configure structured logging (loguru) for the whole application
  - Provide the ChromaDB embedder config with an OpenAI/HuggingFace fallback

Usage:
  from src.config import MODEL_NAME, LATEX_DIR, validate_config
  validate_config()   # call once at the entry point (main.py / app.py)
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

# ---------------------------------------------------------------------------
# 1. Load .env  (safe to call multiple times — dotenv is idempotent)
# ---------------------------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------------------------
# 2. Resolve project paths  (all relative paths are anchored here)
# ---------------------------------------------------------------------------
# config.py lives at:  <project_root>/src/config.py
# So PROJECT_ROOT  is:  <project_root>/
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

SRC_DIR:     Path = PROJECT_ROOT / "src"
LATEX_DIR:   Path = PROJECT_ROOT / "latex"
FIGURES_DIR: Path = LATEX_DIR / "figures"
CHAPTERS_DIR: Path = LATEX_DIR / "chapters"
OUTPUTS_DIR: Path = PROJECT_ROOT / "outputs"
DOCS_DIR:    Path = PROJECT_ROOT / "docs"
TESTS_DIR:   Path = PROJECT_ROOT / "tests"

# Ensure critical output directories exist at import time
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 3. API Keys  (read from environment — NEVER hardcode values here)
# ---------------------------------------------------------------------------
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
SERPER_API_KEY:    str = os.getenv("SERPER_API_KEY", "")
OPENAI_API_KEY:    str = os.getenv("OPENAI_API_KEY", "")

# ---------------------------------------------------------------------------
# 4. Model Constants
# ---------------------------------------------------------------------------
MODEL_NAME: str = os.getenv("CREWAI_MODEL", "claude-sonnet-4-6")
# Full LLM identifier expected by CrewAI's LiteLLM backend:
LLM_IDENTIFIER: str = f"anthropic/{MODEL_NAME}"

# Embedding model (used by ChromaDB memory layer)
EMBEDDING_MODEL: str = "text-embedding-3-small"

# Local fallback model if OpenAI key is absent
EMBEDDING_FALLBACK_MODEL: str = "all-MiniLM-L6-v2"

# ---------------------------------------------------------------------------
# 5. Agent / Crew Runtime Constants
# ---------------------------------------------------------------------------
# Pricing per 1M tokens (Claude 3.5 Sonnet: $3.00 input / $15.00 output)
PRICE_PER_1M_INPUT_TOKENS: float = 3.00
PRICE_PER_1M_OUTPUT_TOKENS: float = 15.00

# Pricing for OpenAI Embeddings (text-embedding-3-small: $0.02 per 1M)
EMBEDDING_PRICE_PER_1M: float = 0.02

# Maximum LLM iterations per agent before CrewAI raises MaxIterationsError
AGENT_MAX_ITER: dict[str, int] = {
    "research_director": 5,
    "deep_researcher":   12,   # PRD: SLAMAndFusionResearcher max_iter=12
    "data_visualizer":   10,   # PRD: VisualizationEngineer max_iter=10
    "latex_author":      15,
    "quality_editor":    5,
}

# Target paper length used in agent prompts
PAPER_TARGET_PAGES: int = 28          # midpoint of 25–30 range
PAPER_MIN_PAGES:    int = 25
PAPER_MAX_PAGES:    int = 30

# ---------------------------------------------------------------------------
# 6. Tool Constants
# ---------------------------------------------------------------------------
MAX_FILE_SIZE_BYTES: int   = 1 * 1024 * 1024   # 1 MB — FileReaderTool limit
CODE_EXECUTOR_TIMEOUT: int = 30                 # seconds — PythonCodeExecutorTool
ARXIV_MAX_RESULTS: int     = 5                  # default ArXiv results per query

# Directories agents are allowed to write into (relative to PROJECT_ROOT)
WRITABLE_DIRS: tuple[str, ...] = ("latex", "outputs", "docs")

# Files that must never be overwritten by an agent
PROTECTED_FILES: tuple[str, ...] = (
    ".env",
    ".gitignore",
    "requirements.txt",
    "src/config.py",
)

# ---------------------------------------------------------------------------
# 7. Logging Configuration (loguru)
# ---------------------------------------------------------------------------
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE:  Path = OUTPUTS_DIR / "researchcrew.log"

# Remove the default stderr sink so we can add our own formatted ones
logger.remove()

# Console sink — human-readable, colourised
logger.add(
    sys.stderr,
    level=LOG_LEVEL,
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> — "
        "<level>{message}</level>"
    ),
)

# File sink — structured, persistent, rotated daily
logger.add(
    str(LOG_FILE),
    level="DEBUG",          # always capture everything to disk
    rotation="10 MB",
    retention="7 days",
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} — {message}",
)

logger.info(f"ResearchCrew starting. PROJECT_ROOT={PROJECT_ROOT}")

# ---------------------------------------------------------------------------
# 8. Embedder Configuration  (used by src/crew.py when building the Crew)
# ---------------------------------------------------------------------------

def get_embedder_config() -> dict:
    """
    Return the ChromaDB embedder config for CrewAI memory.

    Strategy:
      - If OPENAI_API_KEY is present → use text-embedding-3-small (cloud, best quality)
      - Otherwise                    → use all-MiniLM-L6-v2 via HuggingFace (local, no key needed)
    """
    if OPENAI_API_KEY:
        logger.info("Embedder: OpenAI text-embedding-3-small")
        return {
            "provider": "openai",
            "config": {
                "model": EMBEDDING_MODEL,
                "api_key": OPENAI_API_KEY,
            },
        }
    else:
        logger.warning(
            "OPENAI_API_KEY not set — falling back to local HuggingFace embedder. "
            "Memory quality will be slightly lower."
        )
        return {
            "provider": "huggingface",
            "config": {
                "model": EMBEDDING_FALLBACK_MODEL,
            },
        }


# ---------------------------------------------------------------------------
# 9. Config Validation  (call once at application entry point)
# ---------------------------------------------------------------------------

def validate_config() -> None:
    """
    Validate that all required environment variables are set.

    Raises:
        EnvironmentError: If a required key is missing, with a clear fix instruction.
    """
    required: dict[str, str] = {
        "ANTHROPIC_API_KEY": (
            "Get yours at https://console.anthropic.com/ "
            "then add it to your .env file."
        ),
        "SERPER_API_KEY": (
            "Get a free key at https://serper.dev/ "
            "then add it to your .env file."
        ),
    }

    missing: list[str] = []
    for key, instructions in required.items():
        value = os.getenv(key, "")
        if not value or value.strip() == "":
            missing.append(f"  • {key}: {instructions}")

    if missing:
        missing_list = "\n".join(missing)
        raise EnvironmentError(
            f"\n\n[ResearchCrew] Missing required environment variables:\n"
            f"{missing_list}\n\n"
            f"Copy .env.example → .env and fill in the values.\n"
        )

    # Optional key — warn but do not abort
    if not OPENAI_API_KEY:
        logger.warning(
            "OPENAI_API_KEY is not set. "
            "Memory will use a local HuggingFace embedding model instead of OpenAI. "
            "This is fine for development but may reduce research recall quality."
        )

    logger.success("Config validation passed. All required API keys are present.")


# ---------------------------------------------------------------------------
# 10. Quick self-test  (python src/config.py)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== ResearchCrew Config Self-Test ===\n")
    print(f"PROJECT_ROOT : {PROJECT_ROOT}")
    print(f"LATEX_DIR    : {LATEX_DIR}")
    print(f"FIGURES_DIR  : {FIGURES_DIR}")
    print(f"OUTPUTS_DIR  : {OUTPUTS_DIR}")
    print(f"MODEL_NAME   : {MODEL_NAME}")
    print(f"LLM_IDENT    : {LLM_IDENTIFIER}")
    print(f"LOG_LEVEL    : {LOG_LEVEL}")
    print()

    # Show which keys are set (masked) vs missing
    for key in ("ANTHROPIC_API_KEY", "SERPER_API_KEY", "OPENAI_API_KEY"):
        val = os.getenv(key, "")
        status = f"SET ({val[:8]}...)" if val else "NOT SET"
        print(f"{key:25s}: {status}")

    print()
    try:
        validate_config()
    except EnvironmentError as exc:
        print(str(exc))
        sys.exit(1)

    print("\nEmbedder config:")
    import json
    cfg = get_embedder_config()
    # Mask the API key in output
    if "config" in cfg and "api_key" in cfg["config"]:
        cfg["config"]["api_key"] = cfg["config"]["api_key"][:8] + "..."
    print(json.dumps(cfg, indent=2))
