from typing import Any

from ..schemas import (
    OutlineResponse,
    StoryResponse,
)


def build_comic(
    outline: OutlineResponse,
    story: StoryResponse,
    image_paths: list[str] | dict[int, str],
) -> list[dict[str, Any]]:

    story_map = {
        panel.panel_number: panel
        for panel in story.panels
    }

    if isinstance(image_paths, dict):
        image_map = image_paths
    else:
        image_map = {
            index + 1: path
            for index, path in enumerate(image_paths)
        }

    comic = []

    for panel in outline.panels:

        story_panel = story_map.get(
            panel.panel_number
        )

        comic.append(
            {
                "panel_number": panel.panel_number,

                "title": panel.title,

                "scene_description": (
                    panel.scene_description
                ),

                "image_prompt": (
                    panel.image_prompt
                ),

                "image_path": image_map.get(
                    panel.panel_number,
                    "",
                ),

                "caption": (
                    story_panel.caption
                    if story_panel
                    else panel.title
                ),

                "narration": (
                    story_panel.narration
                    if story_panel
                    else panel.scene_description
                ),

                "dialogue": (
                    story_panel.dialogue
                    if story_panel
                    else ""
                ),
            }
        )

    return comic