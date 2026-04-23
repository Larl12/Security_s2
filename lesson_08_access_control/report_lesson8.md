# Отчет по ДЗ 8 «Чужие здесь не ходят»

## Ссылка на GitHub

```text
[вставь ссылку на репозиторий]
```

## Что реализовано

- ролевая модель `user/admin`
- защита от IDOR для `GET /files/{file_id}`
- защищенное удаление через `DELETE /files/{file_id}`
- `GET /files/my` возвращает только файлы текущего пользователя
- `GET /files/all` доступен только администратору
- автотесты безопасности в `test_security.py`

## Структура проекта

```text
lesson_08_access_control/
├── requirements.txt
├── report_lesson8.md
├── test_security.py
└── src
    ├── __init__.py
    └── main.py
```

## Файл test_security.py

```python
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
```

## Команды запуска

```bash
cd ~/project/Security_s2/lesson_08_access_control
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Команды запуска тестов

```bash
cd ~/project/Security_s2/lesson_08_access_control
source venv/bin/activate
pytest -v
```

## Что приложить

- файл `test_security.py`
- скриншот терминала с успешным запуском `pytest -v`

## Деплой на сервер

```bash
git pull
cd ~/project/Security_s2/lesson_08_access_control
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Коммит

```text
Task 8 ready.
```
