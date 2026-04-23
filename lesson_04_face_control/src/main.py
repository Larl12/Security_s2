from fastapi import FastAPI

from src.schemas import UserCreate

app = FastAPI(title="Face Control API")


@app.post("/registration")
def register_user(payload: UserCreate) -> dict[str, str]:
    return {"msg": "User created", "user": payload.username}
