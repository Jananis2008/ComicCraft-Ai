from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_CANDIDATES = [
    BASE_DIR / ".env",
    BASE_DIR / "app" / ".env",
    BASE_DIR / "app" / "services" / ".env",
]

ENV_FILE = next(
    (path for path in ENV_CANDIDATES if path.exists()),
    BASE_DIR / ".env",
)


class Settings(BaseSettings):

    app_name: str = "ComicCraft"
    app_version: str = "1.0.0"

    gemini_api_key: str = ""

    gemini_outline_model: str = "gemini-3.1-flash-lite-preview"
    gemini_story_model: str = "gemini-3.1-pro-preview"

    hf_token: str = ""
    hf_image_model: str = "black-forest-labs/FLUX.1-schnell"
    hf_provider: str = "auto"

    use_mock_ai: bool = False

    image_width: int = 768
    image_height: int = 1024

    max_panels: int = 5

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()


STATIC_DIR = BASE_DIR / "static"

PANELS_DIR = STATIC_DIR / "panels"
EXPORTS_DIR = STATIC_DIR / "exports"
JOBS_DIR = STATIC_DIR / "jobs"


PANELS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

EXPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

JOBS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)