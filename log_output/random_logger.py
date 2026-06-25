import uuid
from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI()

# Generate random string once on startup
random_string = str(uuid.uuid4())


def current_timestamp() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"


@app.get("/status")
async def status():
    return {
        "timestamp": current_timestamp(),
        "random_string": random_string,
    }