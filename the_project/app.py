from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
import os
from pathlib import Path
from datetime import datetime, timedelta
import requests

IMAGE = Path("/data/image.jpg")
STAMP = Path("/data/timestamp.txt")

CACHE_SECONDS = int(os.getenv("CACHE_SECONDS", "600"))
CACHE_TIME = timedelta(seconds=CACHE_SECONDS)

MESSAGE = os.getenv("MESSAGE", "Hello Kubernetes!")

app = FastAPI()

HARDCODED_TODOS = [
    "Buy groceries",
    "Finish Kubernetes exercise",
    "Read FastAPI documentation",
]


def image_is_fresh():
    if not IMAGE.exists() or not STAMP.exists():
        return False

    ts = datetime.fromisoformat(STAMP.read_text())

    return datetime.utcnow() - ts < CACHE_TIME


def download_image():
    r = requests.get("https://picsum.photos/1200")

    IMAGE.write_bytes(r.content)

    STAMP.write_text(datetime.utcnow().isoformat())


@app.get("/image")
def image():
    if not image_is_fresh():
        download_image()

    return FileResponse(IMAGE)


@app.get("/", response_class=HTMLResponse)
def root():
    todo_items = "\n".join(
        f"<li>{todo}</li>" for todo in HARDCODED_TODOS
    )

    return f"""
    <html>
        <body>
            <h1>{MESSAGE}</h1>

            <img src="/image" width="600">

            <h2>Add Todo</h2>

            <form>
                <input
                    type="text"
                    id="todo"
                    name="todo"
                    maxlength="140"
                    placeholder="Enter a todo (max 140 characters)"
                >
                <button type="button">Send</button>
            </form>

            <h2>Todos</h2>

            <ul>
                {todo_items}
            </ul>
        </body>
    </html>
    """