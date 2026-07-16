from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from pathlib import Path
from datetime import datetime, timedelta
import requests
from fastapi.responses import FileResponse

IMAGE = Path("/data/image.jpg")
STAMP = Path("/data/timestamp.txt")

CACHE_SECONDS = int(os.getenv("CACHE_SECONDS", "600"))
CACHE_TIME = timedelta(seconds=CACHE_SECONDS)

MESSAGE = os.getenv("MESSAGE", "Hello Kubernetes!")

app = FastAPI()

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

    return f"""
    <html>
        <body>
            <h1>{MESSAGE}</h1>
            <img src="/image">
        </body>
    </html>
    """