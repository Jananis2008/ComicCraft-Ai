from pathlib import Path

from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)

from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
)

from fastapi.templating import Jinja2Templates

from .config import settings
from .schemas import PromptRequest

from .services.exporters import create_pdf
from .services.gemini_flash import generate_outline
from .services.gemini_pro import generate_story
from .services.image_generator import generate_image
from .services.job_store import create_job, get_job
from .services.layout_builder import build_comic


router = APIRouter()


BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


@router.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "app_name": settings.app_name,
            "error": None,
        },
    )


def generate_comic(
    request_data: PromptRequest,
):

    outline = generate_outline(
        request_data
    )

    story = generate_story(
        outline
    )

    image_by_number = {}

    for panel in outline.panels:

        image_path = generate_image(
            panel
        )

        image_by_number[
            panel.panel_number
        ] = image_path

    comic = build_comic(
        outline=outline,
        story=story,
        image_paths=image_by_number,
    )

    job_id = create_job(
        {
            "request": request_data.model_dump(),
            "outline": outline.model_dump(),
            "story": story.model_dump(),
            "comic": comic,
        }
    )

    return job_id, comic


@router.post(
    "/generate",
    response_class=HTMLResponse,
)
async def generate(
    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form("Alex"),

    setting: str = Form("enchanted forest"),

    tone: str = Form("adventurous"),

    art_style: str = Form("comic book"),

    panel_count: int = Form(5),
):

    try:

        request_data = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
            panel_count=panel_count,
        )

        job_id, comic = generate_comic(
            request_data
        )

        return templates.TemplateResponse(
            request,
            "comic_preview.html",
            {
                "request": request,
                "app_name": settings.app_name,
                "job_id": job_id,
                "comic": comic,
            },
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "request": request,
                "app_name": settings.app_name,
                "error": str(exc),
            },
            status_code=500,
        )


@router.post(
    "/generate-comic/json",
)
async def generate_json(
    request_data: PromptRequest,
):

    try:

        job_id, comic = generate_comic(
            request_data
        )

        return JSONResponse(
            {
                "success": True,
                "job_id": job_id,
                "comic": comic,
            }
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.get(
    "/export/{job_id}",
)
async def export_comic(
    job_id: str,
):

    job = get_job(job_id)

    if not job:

        raise HTTPException(
            status_code=404,
            detail="Comic job not found.",
        )

    pdf_path = create_pdf(
        job_id=job_id,
        comic=job["comic"],
    )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"comic_{job_id}.pdf",
    )


@router.get(
    "/api/jobs/{job_id}",
)
async def get_job_api(
    job_id: str,
):

    job = get_job(job_id)

    if not job:

        raise HTTPException(
            status_code=404,
            detail="Comic job not found.",
        )

    return job