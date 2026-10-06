from ..config import settings

from ..schemas import (
    OutlineResponse,
    StoryPanel,
    StoryResponse,
)

from .gemini_client import gemini_client


def create_mock_story(
    outline: OutlineResponse,
) -> StoryResponse:

    panels = []

    for panel in outline.panels:

        panels.append(
            StoryPanel(
                panel_number=panel.panel_number,
                title=panel.title,
                caption=panel.title,
                narration=panel.scene_description,
                dialogue=(
                    "I can do this! "
                    "The adventure continues!"
                ),
            )
        )

    return StoryResponse(
        panels=panels
    )


def generate_story(
    outline: OutlineResponse,
) -> StoryResponse:

    if (
        settings.use_mock_ai
        or not gemini_client.available
    ):
        return create_mock_story(outline)

    outline_text = "\n\n".join(
        [
            (
                f"Panel {panel.panel_number}\n"
                f"Title: {panel.title}\n"
                f"Scene: {panel.scene_description}\n"
            )
            for panel in outline.panels
        ]
    )

    prompt = f"""
Convert this {len(outline.panels)}-panel outline into a
professional comic script.

OUTLINE:

{outline_text}

For each panel produce:

- panel_number
- title
- caption
- narration
- dialogue

Rules:

- Keep dialogue short.
- Make the narration natural.
- Maintain story continuity.
- Make the ending satisfying.
- Return exactly {len(outline.panels)} panels.
- Return JSON only.
"""

    schema = {
        "type": "OBJECT",
        "properties": {
            "panels": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "panel_number": {
                            "type": "INTEGER"
                        },
                        "title": {
                            "type": "STRING"
                        },
                        "caption": {
                            "type": "STRING"
                        },
                        "narration": {
                            "type": "STRING"
                        },
                        "dialogue": {
                            "type": "STRING"
                        },
                    },
                    "required": [
                        "panel_number",
                        "title",
                        "caption",
                        "narration",
                        "dialogue",
                    ],
                },
            }
        },
        "required": ["panels"],
    }

    try:
        data = gemini_client.generate_json(
            prompt=prompt,
            model=settings.gemini_story_model,
            response_schema=schema,
        )
    except Exception:
        return create_mock_story(outline)

    try:
        return StoryResponse.model_validate(data)
    except Exception:
        return create_mock_story(outline)