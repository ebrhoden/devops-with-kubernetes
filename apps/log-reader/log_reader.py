from fastapi import FastAPI
from pathlib import Path
from pathlib import Path

from fastapi.responses import PlainTextResponse

app = FastAPI()

LOG_FILE = Path("/shared/log.txt")
COUNTER_FILE = Path("/shared/counter.txt")

@app.get("/status")
async def status():

    log = LOG_FILE.read_text() if LOG_FILE.exists() else ""

    if COUNTER_FILE.exists():
        counter = COUNTER_FILE.read_text().strip()
    else:
        counter = "0"

    return PlainTextResponse(
        f"{log}\nPing / Pongs: {counter}"
    )