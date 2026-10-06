import io
from pathlib import Path

from PIL import Image, ImageDraw

from ..config import (
    PANELS_DIR,
    settings,
)

from ..schemas import Panel


try:
    from huggingface_hub import InferenceClient
except ImportError:
    InferenceClient = None


def create_placeholder_image(
    panel: Panel,
    output_path: Path,
) -> None:

    image = Image.new(
        "RGB",
        (
            settings.image_width,
            settings.image_height,
        ),
        "white",
    )

    draw = ImageDraw.Draw(image)

    margin = 40

    draw.rectangle(
        (
            margin,
            margin,
            settings.image_width - margin,
            settings.image_height - margin,
        ),
        outline="black",
        width=4,
    )

    draw.text(
        (
            margin + 20,
            margin + 20,
        ),
        (
            f"PANEL {panel.panel_number}\n"
            f"{panel.title}"
        ),
        fill="black",
    )

    draw.text(
        (
            margin + 20,
            margin + 120,
        ),
        panel.scene_description,
        fill="black",
    )

    image.save(
        output_path,
        format="PNG",
    )


def generate_image(
    panel: Panel,
) -> str:

    filename = (
        f"panel_{panel.panel_number}.png"
    )

    output_path = (
        PANELS_DIR / filename
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if (
        settings.use_mock_ai
        or not settings.hf_token
        or InferenceClient is None
    ):

        create_placeholder_image(
            panel,
            output_path,
        )

        return f"/static/panels/{filename}"

    try:

        if settings.hf_provider == "auto":

            client = InferenceClient(
                api_key=settings.hf_token
            )

        else:

            client = InferenceClient(
                provider=settings.hf_provider,
                api_key=settings.hf_token,
            )

        generated = client.text_to_image(
            prompt=panel.image_prompt,
            model=settings.hf_image_model,
        )

        if hasattr(generated, "save"):
            generated.save(output_path)
        else:
            image = Image.open(io.BytesIO(generated))
            image.save(output_path)

    except Exception:

        create_placeholder_image(
            panel,
            output_path,
        )

    return f"/static/panels/{filename}"