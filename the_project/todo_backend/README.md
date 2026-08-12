# Todo Backend

## Source Code

This project consists of a FastAPI application that manages todo items.

The application exposes:

* `GET /todos` to return the current list of todos.
* `POST /todos` to create a new todo.

The todos are stored in memory.

The application is packaged as the following Docker image:

* `ebrhoden/todo_backend:0.0.2`

## Application Architecture

The Todo Backend is responsible only for managing todo items.

It does not serve the HTML interface or random images. Those responsibilities belong to the Todo App.

The Todo App communicates with this application over HTTP through the Kubernetes Service `todo-backend`.

## API

### Get todos

```http
GET /todos
```

Returns the current list of todos.

Example response:

```json
[
  {
    "id": 1,
    "text": "Buy groceries"
  },
  {
    "id": 2,
    "text": "Finish Kubernetes exercise"
  },
  {
    "id": 3,
    "text": "Read FastAPI documentation"
  }
]
```

### Create a todo

```http
POST /todos
```

The request body should contain the todo text:

```json
{
  "text": "Learn Kubernetes networking"
}
```

Example response:

```json
{
  "id": 4,
  "text": "Learn Kubernetes networking"
}
```

## Deploy the application

Apply the Kubernetes manifests:

```bash
kubectl apply -f todo-backend-deployment.yaml
kubectl apply -f todo-backend-service.yaml
```

Verify that the Pod is running:

```bash
kubectl get pods
```

Verify that the Service was created:

```bash
kubectl get svc
```

The Service should be called:

```text
todo-backend
```

## Verify the application

You can port-forward the backend Service to access it from your local machine:

```bash
kubectl port-forward svc/todo-backend 8000:8000
```

Open:

```text
http://localhost:8000/todos
```

You should see the current list of todos.

## Verify pod-to-pod communication

The backend is intended to be accessed by other applications inside the Kubernetes cluster.

The Todo App can reach the backend using the Kubernetes Service DNS name:

```text
http://todo-backend:8000
```

For example:

```bash
kubectl exec -it deploy/todoapp-dep -- \
  wget -qO- http://todo-backend:8000/todos
```

The command should return the current list of todos.

## Verify the deployment

List the running resources:

```bash
kubectl get deployments
kubectl get services
kubectl get pods
```

The `todo-backend` Deployment should have a running Pod, and the `todo-backend` Service should have an endpoint pointing to that Pod.
