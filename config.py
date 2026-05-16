# config.py
# ACSIF API and runtime configuration

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
MODEL = os.getenv("ACSIF_MODEL", "gemini-2.0-flash").strip()

# Set ACSIF_USE_LLM=false in .env if you want a completely offline demo.
_raw_use_llm = os.getenv("ACSIF_USE_LLM", "true").strip().lower()
USE_LLM = _raw_use_llm not in {"false", "0", "no", "off"}

MAX_TOKENS = 1024

# The code intentionally does NOT crash when API key is missing.
# This makes the project demo-safe even when Gemini quota is exhausted.
LLM_AVAILABLE = bool(GEMINI_API_KEY) and USE_LLM
