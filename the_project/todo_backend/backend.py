from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


todos = [
    {"id": 1, "text": "Buy groceries"},
    {"id": 2, "text": "Finish Kubernetes exercise"},
    {"id": 3, "text": "Read FastAPI documentation"},
]


class Todo(BaseModel):
    text: str


@app.get("/todos")
def get_todos():
    return todos


@app.post("/todos")
def create_todo(todo: Todo):
    new_todo = {
        "id": len(todos) + 1,
        "text": todo.text,
    }

    todos.append(new_todo)

    return new_todo