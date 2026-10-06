import json
from typing import Any, Optional

from google import genai
from google.genai import types

from ..config import settings


class GeminiClient:

    def __init__(self):

        self.client = None

        if settings.gemini_api_key:
            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

    @property
    def available(self) -> bool:
        return self.client is not None

    def generate_json(
        self,
        prompt: str,
        model: str,
        response_schema: Optional[
            dict[str, Any]
        ] = None,
    ) -> dict[str, Any]:

        if not self.client:
            raise RuntimeError(
                "Gemini API key is not configured."
            )

        config = types.GenerateContentConfig(
            temperature=0.7,
            response_mime_type="application/json",
            response_schema=response_schema,
        )

        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        try:
            return json.loads(response.text)

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Gemini returned invalid JSON."
            ) from exc


gemini_client = GeminiClient()