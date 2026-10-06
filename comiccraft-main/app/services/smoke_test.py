from app.schemas import PromptRequest

from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic
from app.services.job_store import create_job, get_job
from app.services.exporters import create_pdf


def main():

    print("Starting ComicCraft smoke test...")

    request = PromptRequest(
        story_prompt=(
            "A young hero discovers "
            "a magical portal."
        ),
        character_name="Alex",
        setting="magical forest",
        tone="adventurous",
        art_style="comic book",
    )

    print("1. Generating outline...")

    outline = generate_outline(request)

    assert len(outline.panels) == 5

    print("2. Generating story...")

    story = generate_story(outline)

    assert len(story.panels) == 5

    print("3. Generating images...")

    image_paths = []

    for panel in outline.panels:

        image_path = generate_image(panel)

        image_paths.append(image_path)

    assert len(image_paths) == 5

    print("4. Building comic...")

    comic = build_comic(
        outline,
        story,
        image_paths,
    )

    assert len(comic) == 5

    print("5. Creating job...")

    job_id = create_job(
        {
            "request": request.model_dump(),
            "outline": outline.model_dump(),
            "story": story.model_dump(),
            "comic": comic,
        }
    )

    assert get_job(job_id) is not None

    print("6. Creating PDF...")

    pdf_path = create_pdf(
        job_id,
        comic,
    )

    assert pdf_path.exists()

    print()
    print("====================================")
    print("ComicCraft smoke test PASSED")
    print("====================================")


if __name__ == "__main__":
    main()