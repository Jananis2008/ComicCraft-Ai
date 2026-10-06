from pathlib import Path

from fpdf import FPDF

from ..config import (
    EXPORTS_DIR,
    STATIC_DIR,
)


def create_pdf(
    job_id: str,
    comic: list[dict],
) -> Path:

    output_path = (
        EXPORTS_DIR /
        f"comic_{job_id}.pdf"
    )

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )

    for panel in comic:

        pdf.add_page()

        # Title
        pdf.set_font(
            "Helvetica",
            "B",
            18,
        )

        pdf.cell(
            0,
            12,
            (
                f"Panel {panel['panel_number']}: "
                f"{panel['title']}"
            ),
            new_x="LMARGIN",
            new_y="NEXT",
        )

        # Image
        web_path = panel["image_path"]

        relative_path = (
            web_path
            .replace("/static/", "")
            .lstrip("/")
        )

        image_path = (
            STATIC_DIR / relative_path
        )

        if image_path.exists():

            pdf.image(
                str(image_path),
                x=20,
                y=35,
                w=170,
                h=125,
            )

        # Caption
        pdf.set_y(168)

        pdf.set_font(
            "Helvetica",
            "B",
            11,
        )

        pdf.cell(
            0,
            8,
            "Caption",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        pdf.set_font(
            "Helvetica",
            "",
            10,
        )

        pdf.multi_cell(
            170,
            6,
            panel["caption"],
        )

        pdf.ln(3)

        # Narration
        pdf.set_font(
            "Helvetica",
            "B",
            11,
        )

        pdf.cell(
            0,
            8,
            "Narration",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        pdf.set_font(
            "Helvetica",
            "",
            10,
        )

        pdf.multi_cell(
            170,
            6,
            panel["narration"],
        )

        pdf.ln(3)

        # Dialogue
        pdf.set_font(
            "Helvetica",
            "B",
            11,
        )

        pdf.cell(
            0,
            8,
            "Dialogue",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        pdf.set_font(
            "Helvetica",
            "",
            10,
        )

        pdf.multi_cell(
            170,
            6,
            panel["dialogue"],
        )

    pdf.output(
        str(output_path)
    )

    return output_path