from pathlib import Path
from typing import Annotated
from uuid import uuid4

import filetype
from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

app = FastAPI(title="Secure File Storage")

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 2 * 1024 * 1024
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}

users_db = {
    "alice": {"id": 1, "username": "alice", "role": "user"},
    "bob": {"id": 2, "username": "bob", "role": "user"},
    "admin": {"id": 3, "username": "admin", "role": "admin"},
}

files_db: list[dict] = []
next_file_id = 1


def get_current_user(x_user: Annotated[str | None, Header()] = None) -> dict:
    if not x_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    user = users_db.get(x_user)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown user")

    return user


def get_file_by_id(file_id: int) -> dict:
    file_record = next((item for item in files_db if item["id"] == file_id), None)
    if not file_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return file_record


def check_file_permissions(file_id: int, user: dict = Depends(get_current_user)) -> dict:
    file_record = get_file_by_id(file_id)
    is_owner = file_record["owner"] == user["username"]
    is_admin = user["role"] == "admin"

    if not (is_owner or is_admin):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    return file_record


@app.get("/files/my")
def get_my_files(user: dict = Depends(get_current_user)) -> dict[str, list[dict]]:
    user_files = [item for item in files_db if item["owner"] == user["username"]]
    return {"files": user_files}


@app.post("/files/upload")
async def upload_file(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
) -> dict:
    global next_file_id

    head = await file.read(2048)
    kind = filetype.guess(head)
    if kind is None or kind.mime not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only JPEG and PNG files are allowed")

    await file.seek(0)

    extension = ".jpg" if kind.mime == "image/jpeg" else ".png"
    physical_name = f"{uuid4()}{extension}"
    destination = STORAGE_DIR / physical_name

    total_size = 0

    try:
        with destination.open("wb") as buffer:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break

                total_size += len(chunk)
                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="File is too large",
                    )

                buffer.write(chunk)
    except HTTPException:
        if destination.exists():
            destination.unlink()
        raise

    file_record = {
        "id": next_file_id,
        "owner": user["username"],
        "original_name": file.filename or physical_name,
        "path": str(destination),
        "size": total_size,
        "mime_type": kind.mime,
    }
    files_db.append(file_record)
    next_file_id += 1

    return {
        "msg": "File uploaded",
        "file_id": file_record["id"],
        "original_name": file_record["original_name"],
        "stored_name": physical_name,
        "size": total_size,
    }


@app.get("/files/{file_id}/download")
def download_file(file_record: dict = Depends(check_file_permissions)) -> FileResponse:
    file_path = Path(file_record["path"])
    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stored file not found")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=file_record["original_name"],
        headers={"Content-Disposition": f'attachment; filename="{file_record["original_name"]}"'},
    )
