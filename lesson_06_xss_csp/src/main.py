from typing import List

import bleach
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from markupsafe import Markup

app = FastAPI(title="Comments Wall")
templates = Jinja2Templates(directory="templates")

raw_comments: List[str] = []

ALLOWED_TAGS = ["b", "i", "u", "em", "strong"]
CSP_POLICY = "default-src 'self'; script-src 'self'; style-src 'self'"


def sanitize_comment(text: str) -> str:
    return bleach.clean(text, tags=ALLOWED_TAGS, attributes={}, strip=True)


@app.get("/comments")
def get_comments(request: Request):
    sanitized_comments = [Markup(sanitize_comment(comment)) for comment in raw_comments]
    return templates.TemplateResponse(
        "comments.html",
        {
            "request": request,
            "title": "Safe Comments",
            "comments": sanitized_comments,
            "post_url": "/comments",
            "mode": "safe",
        },
        headers={"Content-Security-Policy": CSP_POLICY},
    )


@app.post("/comments")
def create_comment(comment: str = Form(...)):
    raw_comments.append(comment)
    return RedirectResponse(url="/comments", status_code=303)


@app.get("/comments/unsafe")
def get_comments_unsafe(request: Request):
    return templates.TemplateResponse(
        "comments.html",
        {
            "request": request,
            "title": "Unsafe Comments Demo",
            "comments": raw_comments,
            "post_url": "/comments/unsafe",
            "mode": "unsafe",
        },
    )


@app.post("/comments/unsafe")
def create_comment_unsafe(comment: str = Form(...)):
    raw_comments.append(comment)
    return RedirectResponse(url="/comments/unsafe", status_code=303)
