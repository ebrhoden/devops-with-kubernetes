from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse

import os
from pathlib import Path
from datetime import datetime, timedelta
from urllib.parse import parse_qs

import requests

DATA_DIR = Path(os.getenv("DATA_DIR"))

IMAGE = DATA_DIR / "image.jpg"
STAMP = DATA_DIR / "timestamp.txt"

CACHE_SECONDS = int(os.getenv("CACHE_SECONDS"))
CACHE_TIME = timedelta(seconds=CACHE_SECONDS)

MESSAGE = os.getenv("MESSAGE")

BACKEND_URL = os.getenv("BACKEND_URL")
IMAGE_URL = os.getenv("IMAGE_URL")

app = FastAPI()

def image_is_fresh():
    if not IMAGE.exists() or not STAMP.exists():
        return False

    ts = datetime.fromisoformat(STAMP.read_text())

    return datetime.utcnow() - ts < CACHE_TIME


def download_image():
    r = requests.get(IMAGE_URL)
    r.raise_for_status()

    IMAGE.write_bytes(r.content)

    STAMP.write_text(datetime.utcnow().isoformat())


def get_todos():
    response = requests.get(f"{BACKEND_URL}/todos")
    response.raise_for_status()

    return response.json()


@app.get("/image")
def image():
    if not image_is_fresh():
        download_image()

    return FileResponse(IMAGE)


@app.post("/todos")
async def create_todo(request: Request):
    body = await request.body()

    form = parse_qs(body.decode())

    todo_text = form.get("todo", [""])[0].strip()

    if todo_text:
        response = requests.post(
            f"{BACKEND_URL}/todos",
            json={"text": todo_text},
        )

        response.raise_for_status()

    return RedirectResponse("/", status_code=303)


@app.get("/", response_class=HTMLResponse)
def root():

    todos = get_todos()

    todo_items = "\n".join(
        f"<li>{todo['text']}</li>"
        for todo in todos
    )

    return f"""
    <html>
        <body>

            <h1>{MESSAGE}</h1>

            <img src="/image" width="600">

            <h2>Add Todo</h2>

            <form method="POST" action="/todos">
                <input
                    type="text"
                    id="todo"
                    name="todo"
                    maxlength="140"
                    placeholder="Enter a todo (max 140 characters)"
                    required
                >

                <button type="submit">Send</button>
            </form>

            <h2>Todos</h2>

            <ul>
                {todo_items}
            </ul>

        </body>
    </html>
    """
