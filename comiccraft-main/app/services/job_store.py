import json
import uuid
from typing import Any

from ..config import JOBS_DIR


def create_job(
    data: dict[str, Any],
) -> str:

    job_id = uuid.uuid4().hex

    file_path = (
        JOBS_DIR / f"{job_id}.json"
    )

    file_path.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return job_id


def get_job(
    job_id: str,
) -> dict[str, Any] | None:

    file_path = (
        JOBS_DIR / f"{job_id}.json"
    )

    if not file_path.exists():
        return None

    return json.loads(
        file_path.read_text(
            encoding="utf-8"
        )
    )