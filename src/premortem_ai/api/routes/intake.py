"""
intake.py

FastAPI endpoint for PreMortem intake submissions.

Responsibilities:
- Accept file uploads + optional typed description
- Persist files temporarily
- Call deterministic intake layer
- Return structured intake output

NO reasoning logic lives here.
"""

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List, Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from premortem_ai.intake import intake_submission
from premortem_ai.core.logger import info, error

router = APIRouter(prefix="/intake", tags=["intake"])


@router.post("")
async def submit_intake(
    files: Optional[List[UploadFile]] = File(default=None),
    typed_description: Optional[str] = Form(default=None),
):
    """
    Submit a PreMortem intake request.
    """

    info("Received intake submission")

    try:
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            file_paths: List[Path] = []

            if files:
                for upload in files:
                    dest = tmp_path / upload.filename
                    contents = await upload.read()
                    dest.write_bytes(contents)
                    file_paths.append(dest)

            result = intake_submission(
                file_paths=file_paths if file_paths else None,
                typed_description=typed_description,
                user_id="anonymous",  # auth comes later
            )

            return result

    except ValueError as exc:
        # deterministic intake validation errors
        error(f"Intake validation failed: {exc}")
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception as exc:
        # unexpected server-side failure
        error(f"Unhandled intake error: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Internal intake error",
        ) from exc
