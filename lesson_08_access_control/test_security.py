from fastapi.testclient import TestClient

from src.main import app, reset_files_db

client = TestClient(app)


def setup_function() -> None:
    reset_files_db()


def test_1_idor_user_cannot_read_foreign_file() -> None:
    response = client.get("/files/2", headers={"X-User": "alice"})
    assert response.status_code == 404


def test_2_user_can_read_own_file() -> None:
    response = client.get("/files/1", headers={"X-User": "alice"})
    assert response.status_code == 200
    assert response.json()["owner"] == "alice"


def test_3_admin_can_delete_foreign_file() -> None:
    delete_response = client.delete("/files/2", headers={"X-User": "admin"})
    assert delete_response.status_code == 200

    list_response = client.get("/files/all", headers={"X-User": "admin"})
    remaining_ids = [file["id"] for file in list_response.json()["files"]]
    assert 2 not in remaining_ids


def test_my_files_returns_only_current_user_files() -> None:
    response = client.get("/files/my", headers={"X-User": "bob"})
    assert response.status_code == 200
    owners = {file["owner"] for file in response.json()["files"]}
    assert owners == {"bob"}
