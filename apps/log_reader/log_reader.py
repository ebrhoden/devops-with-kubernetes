from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pathlib import Path
import httpx

app = FastAPI()

LOG_FILE = Path("/shared/log.txt")

PINGPONG_URL = "http://pingpong-svc:2345/pings"

@app.get("/status")
async def status():

    log = LOG_FILE.read_text() if LOG_FILE.exists() else ""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(PINGPONG_URL)
            counter = response.text.strip()
    except Exception:
        counter = "0"

    return PlainTextResponse(
        f"{log}\nPing / Pongs: {counter}"
    )