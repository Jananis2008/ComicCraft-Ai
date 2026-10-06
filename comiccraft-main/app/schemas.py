from typing import List

from pydantic import BaseModel, Field, field_validator


class PromptRequest(BaseModel):

    story_prompt: str = Field(
        min_length=5,
        max_length=2000,
    )

    character_name: str = Field(
        default="Alex",
        min_length=1,
        max_length=80,
    )

    setting: str = Field(
        default="enchanted forest",
        min_length=1,
        max_length=120,
    )

    tone: str = Field(
        default="adventurous",
        min_length=1,
        max_length=80,
    )

    art_style: str = Field(
        default="comic book",
        min_length=1,
        max_length=100,
    )

    panel_count: int = Field(
        default=5,
        ge=1,
        le=5,
    )

    @field_validator(
        "story_prompt",
        "character_name",
        "setting",
        "tone",
        "art_style",
    )
    @classmethod
    def clean_values(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Value cannot be empty."
            )

        return value


class Panel(BaseModel):

    panel_number: int

    title: str

    scene_description: str

    image_prompt: str


class OutlineResponse(BaseModel):

    panels: List[Panel]


class StoryPanel(BaseModel):

    panel_number: int

    title: str

    caption: str

    narration: str

    dialogue: str


class StoryResponse(BaseModel):

    panels: List[StoryPanel]