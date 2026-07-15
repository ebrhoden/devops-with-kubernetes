from fastapi import FastAPI
from pathlib import Path

app = FastAPI()

LOG_FILE = Path("/shared/log.txt")


@app.get("/status")
async def status():
    if LOG_FILE.exists():
        return {"content": LOG_FILE.read_text()}

    return {"content": "Log file not ready"}