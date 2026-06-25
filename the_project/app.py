from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

MESSAGE = os.getenv("MESSAGE", "Hello Kubernetes!")

@app.get("/", response_class=HTMLResponse)
def root():
    return f"""
    <html>
        <body>
            <h1>{MESSAGE}</h1>
        </body>
    </html>
    """