from ..config import settings

from ..schemas import (
    OutlineResponse,
    Panel,
    PromptRequest,
)

from .gemini_client import gemini_client


def create_mock_outline(
    request: PromptRequest,
) -> OutlineResponse:

    panel_count = min(
        max(1, request.panel_count),
        settings.max_panels,
    )

    panel_templates = [
        (
            "The Beginning",
            f"{request.character_name} enters the {request.setting}.",
            f"{request.character_name} entering a {request.setting}, {request.art_style}, cinematic comic panel",
        ),
        (
            "The Discovery",
            f"{request.character_name} discovers something mysterious.",
            f"{request.character_name} discovering a mysterious glowing object in the {request.setting}, {request.art_style}",
        ),
        (
            "The Challenge",
            "A difficult challenge suddenly appears.",
            f"{request.character_name} facing a dramatic challenge in the {request.setting}, {request.art_style}",
        ),
        (
            "The Solution",
            f"{request.character_name} finds a creative solution.",
            f"{request.character_name} solving the challenge using courage and creativity, {request.art_style}",
        ),
        (
            "The Ending",
            f"{request.character_name} completes the adventure successfully.",
            f"{request.character_name} celebrating in the {request.setting}, happy ending, {request.art_style}",
        ),
    ]

    panels = [
        Panel(
            panel_number=index,
            title=title,
            scene_description=scene_description,
            image_prompt=image_prompt,
        )
        for index, (title, scene_description, image_prompt) in enumerate(
            panel_templates[:panel_count],
            start=1,
        )
    ]

    return OutlineResponse(
        panels=panels
    )


def generate_outline(
    request: PromptRequest,
) -> OutlineResponse:

    panel_count = min(
        max(1, request.panel_count),
        settings.max_panels,
    )

    if (
        settings.use_mock_ai
        or not gemini_client.available
    ):
        return create_mock_outline(request)

    prompt = f"""
Create a {panel_count}-panel comic story outline.

Story:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Requirements:

- Create exactly {panel_count} panels.
- Make the story coherent.
- Give every panel a title.
- Give every panel a scene description.
- Give every panel a detailed image prompt.
- Keep the main character visually consistent.

Return JSON only.
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
                        "scene_description": {
                            "type": "STRING"
                        },
                        "image_prompt": {
                            "type": "STRING"
                        },
                    },
                    "required": [
                        "panel_number",
                        "title",
                        "scene_description",
                        "image_prompt",
                    ],
                },
            }
        },
        "required": ["panels"],
    }

    try:
        data = gemini_client.generate_json(
            prompt=prompt,
            model=settings.gemini_outline_model,
            response_schema=schema,
        )
    except Exception:
        return create_mock_outline(request)

    try:
        result = OutlineResponse.model_validate(data)
    except Exception:
        return create_mock_outline(request)

    if len(result.panels) != panel_count:
        return create_mock_outline(request)

    return result