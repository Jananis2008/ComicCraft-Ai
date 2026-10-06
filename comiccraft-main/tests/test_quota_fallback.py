import unittest
from app.schemas import OutlineResponse, PromptRequest
from app.services import gemini_flash, gemini_pro


class QuotaFallbackTests(unittest.TestCase):
    def test_generate_outline_falls_back_when_gemini_quota_is_exhausted(self):
        original = gemini_flash.gemini_client.generate_json
        gemini_flash.gemini_client.generate_json = lambda **kwargs: (_ for _ in ()).throw(RuntimeError("429 RESOURCE_EXHAUSTED"))
        try:
            request = PromptRequest(
                story_prompt="A hero enters a magical forest",
                character_name="Alex",
                setting="enchanted forest",
                tone="adventurous",
                art_style="comic book",
            )
            outline = gemini_flash.generate_outline(request)
            self.assertIsInstance(outline, OutlineResponse)
            self.assertEqual(len(outline.panels), 5)
        finally:
            gemini_flash.gemini_client.generate_json = original

    def test_generate_outline_respects_requested_panel_count(self):
        original = gemini_flash.gemini_client.generate_json
        gemini_flash.gemini_client.generate_json = lambda **kwargs: {
            "panels": [
                {
                    "panel_number": 1,
                    "title": "Beginning",
                    "scene_description": "A hero enters the forest",
                    "image_prompt": "Hero enters forest",
                },
                {
                    "panel_number": 2,
                    "title": "Discovery",
                    "scene_description": "They discover a hidden cave",
                    "image_prompt": "Hero finds hidden cave",
                },
                {
                    "panel_number": 3,
                    "title": "Ending",
                    "scene_description": "The mystery is solved",
                    "image_prompt": "Hero solves mystery",
                },
            ]
        }
        try:
            request = PromptRequest(
                story_prompt="A hero enters a magical forest",
                character_name="Alex",
                setting="enchanted forest",
                tone="adventurous",
                art_style="comic book",
                panel_count=3,
            )
            outline = gemini_flash.generate_outline(request)
            self.assertIsInstance(outline, OutlineResponse)
            self.assertEqual(len(outline.panels), 3)
        finally:
            gemini_flash.gemini_client.generate_json = original

    def test_generate_story_falls_back_when_gemini_quota_is_exhausted(self):
        original = gemini_pro.gemini_client.generate_json
        gemini_pro.gemini_client.generate_json = lambda **kwargs: (_ for _ in ()).throw(RuntimeError("429 RESOURCE_EXHAUSTED"))
        try:
            outline = OutlineResponse(
                panels=[
                    {
                        "panel_number": 1,
                        "title": "Beginning",
                        "scene_description": "A hero enters the forest",
                        "image_prompt": "Hero in forest",
                    },
                    {
                        "panel_number": 2,
                        "title": "Discovery",
                        "scene_description": "They find a glowing stone",
                        "image_prompt": "Hero discovers glowing stone",
                    },
                    {
                        "panel_number": 3,
                        "title": "Challenge",
                        "scene_description": "A storm races in",
                        "image_prompt": "Storm hits forest",
                    },
                    {
                        "panel_number": 4,
                        "title": "Solution",
                        "scene_description": "They learn the stone controls the wind",
                        "image_prompt": "Hero uses stone to calm storm",
                    },
                    {
                        "panel_number": 5,
                        "title": "Ending",
                        "scene_description": "The forest is peaceful again",
                        "image_prompt": "Hero celebrates in forest",
                    },
                ]
            )
            story = gemini_pro.generate_story(outline)
            self.assertEqual(len(story.panels), 5)
        finally:
            gemini_pro.gemini_client.generate_json = original

    def test_panel_images_follow_panel_numbers_when_outline_order_changes(self):
        outline = OutlineResponse(
            panels=[
                {"panel_number": 1, "title": "Start", "scene_description": "Start", "image_prompt": "Prompt 1"},
                {"panel_number": 3, "title": "Middle", "scene_description": "Middle", "image_prompt": "Prompt 3"},
                {"panel_number": 2, "title": "Bridge", "scene_description": "Bridge", "image_prompt": "Prompt 2"},
                {"panel_number": 5, "title": "End", "scene_description": "End", "image_prompt": "Prompt 5"},
                {"panel_number": 4, "title": "Climax", "scene_description": "Climax", "image_prompt": "Prompt 4"},
            ]
        )
        story = gemini_pro.create_mock_story(outline)
        comic = build_comic(
            outline=outline,
            story=story,
            image_paths=["/p1", "/p2", "/p3", "/p4", "/p5"],
        )

        self.assertEqual(comic[0]["image_path"], "/p1")
        self.assertEqual(comic[1]["image_path"], "/p2")
        self.assertEqual(comic[2]["image_path"], "/p3")
        self.assertEqual(comic[3]["image_path"], "/p4")
        self.assertEqual(comic[4]["image_path"], "/p5")


from app.services.layout_builder import build_comic


if __name__ == "__main__":
    unittest.main()
