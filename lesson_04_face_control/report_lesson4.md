# Отчет по ДЗ 4 «Фейс-контроль»

## Ссылка на GitHub

```text
[вставь ссылку на репозиторий]
```

## Коммит

```text
Task 4 ready.
```

## Структура проекта

```text
lesson_04_face_control/
├── requirements.txt
├── report_lesson4.md
└── src
    ├── main.py
    └── schemas.py
```

## Что реализовано

- `FastAPI` приложение с эндпоинтом `POST /registration`
- `Pydantic` схема `UserCreate`
- валидация `username` по длине и шаблону
- валидация `email` через `EmailStr`
- валидация `age` через `Field(ge=18, le=100)`
- кастомная проверка сложности пароля
- проверка совпадения `password` и `confirm_password`

## Команды запуска

```bash
cd ~/project/Security_s2/lesson_04_face_control
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Swagger

Открыть в браузере:

```text
http://127.0.0.1:8000/docs
```

## Пример валидного запроса

```json
{
  "username": "User123",
  "email": "user@example.com",
  "password": "Strong1!",
  "confirm_password": "Strong1!",
  "age": 21
}
```

## Ожидаемый успешный ответ

```json
{
  "msg": "User created",
  "user": "User123"
}
```

## Что показать в отчете

- запущенный `uvicorn` на Linux / WSL
- открытую страницу `/docs`
- успешный запрос с валидными данными
- невалидный запрос, который возвращает `422`

## Деплой на сервер

Команды:

```bash
git pull
cd lesson_04_face_control
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000
```
