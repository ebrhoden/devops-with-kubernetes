from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pathlib import Path

app = FastAPI()

COUNTER_FILE = Path("/shared/counter.txt")

def get_counter():
    if not COUNTER_FILE.exists():
        COUNTER_FILE.write_text("0")
    return int(COUNTER_FILE.read_text())

def set_counter(value):
    COUNTER_FILE.write_text(str(value))

@app.get("/pingpong", response_class=PlainTextResponse)
async def pingpong():
    counter = get_counter()
    set_counter(counter + 1)
    return f"pong {counter}"

@app.get("/pings", response_class=PlainTextResponse)
async def pings():
    return str(get_counter())