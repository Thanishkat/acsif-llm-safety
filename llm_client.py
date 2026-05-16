# core/llm_client.py
# Safe Gemini wrapper with offline fallback.

from typing import Optional

from config import GEMINI_API_KEY, LLM_AVAILABLE, MODEL

try:
    import google.generativeai as genai
    from google.api_core.exceptions import ResourceExhausted
except Exception:  # Package missing or unavailable
    genai = None
    ResourceExhausted = Exception


class LLMClient:
    """
    Small wrapper around Gemini.

    Design goal:
    - If Gemini works, use it.
    - If Gemini quota is exhausted or key is missing, do not crash.
    - Always return a usable fallback for demo stability.
    """

    def __init__(self, model_name: str = MODEL):
        self.model_name = model_name
        self.available = False
        self.model = None
        self.last_error: Optional[str] = None

        if LLM_AVAILABLE and genai is not None:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = genai.GenerativeModel(self.model_name)
                self.available = True
            except Exception as exc:
                self.last_error = str(exc)
                self.available = False

    def generate(self, prompt: str, fallback: str) -> str:
        """
        Generate text using Gemini. If anything fails, return fallback.
        """
        if not self.available or self.model is None:
            return fallback

        try:
            response = self.model.generate_content(prompt)
            text = getattr(response, "text", None)
            if text and text.strip():
                return text.strip()
            return fallback

        except ResourceExhausted as exc:
            self.last_error = f"Gemini quota exhausted: {exc}"
            return fallback

        except Exception as exc:
            self.last_error = f"Gemini API error: {exc}"
            return fallback
