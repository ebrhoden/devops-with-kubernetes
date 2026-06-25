from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

# In-memory counter
counter = 0


@app.get("/pingpong", response_class=PlainTextResponse)
async def pingpong():
    global counter

    response = f"pong {counter}"
    counter += 1

    return response