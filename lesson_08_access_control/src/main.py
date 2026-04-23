from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Response, status

app = FastAPI(title="Access Control Demo")

users_db = {
    "alice": {"id": 1, "username": "alice", "role": "user"},
    "bob": {"id": 2, "username": "bob", "role": "user"},
    "admin": {"id": 3, "username": "admin", "role": "admin"},
}

INITIAL_FILES = [
    {"id": 1, "filename": "report_alice.pdf", "owner": "alice", "size": 1024},
    {"id": 2, "filename": "photo_bob.jpg", "owner": "bob", "size": 2048},
    {"id": 3, "filename": "admin_keys.txt", "owner": "admin", "size": 12},
]

files_db = [file.copy() for file in INITIAL_FILES]


def reset_files_db() -> None:
    global files_db
    files_db = [file.copy() for file in INITIAL_FILES]


def get_current_user(x_user: Annotated[str | None, Header()] = None) -> dict:
    if not x_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    user = users_db.get(x_user)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown user")

    return user


def get_file_by_id(file_id: int) -> dict:
    file = next((item for item in files_db if item["id"] == file_id), None)
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return file


def check_file_permissions(file_id: int, user: dict = Depends(get_current_user)) -> dict:
    file = get_file_by_id(file_id)
    is_owner = file["owner"] == user["username"]
    is_admin = user["role"] == "admin"

    if not (is_owner or is_admin):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    return file


@app.get("/files/my")
def get_my_files(user: dict = Depends(get_current_user)) -> dict[str, list[dict]]:
    my_files = [file for file in files_db if file["owner"] == user["username"]]
    return {"files": my_files}


@app.get("/files/all")
def get_all_files(user: dict = Depends(get_current_user)) -> dict[str, list[dict]]:
    if user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")

    return {"files": files_db}


@app.get("/files/{file_id}")
def read_file(file: dict = Depends(check_file_permissions)) -> dict:
    return file


@app.delete("/files/{file_id}")
def delete_file(
    file: dict = Depends(check_file_permissions),
    user: dict = Depends(get_current_user),
) -> dict[str, str]:
    global files_db

    is_owner = file["owner"] == user["username"]
    is_admin = user["role"] == "admin"
    if not (is_owner or is_admin):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    files_db = [item for item in files_db if item["id"] != file["id"]]
    return {"msg": "File deleted", "file": file["filename"]}


@app.post("/test/reset", status_code=status.HTTP_204_NO_CONTENT)
def reset_test_data() -> Response:
    reset_files_db()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
