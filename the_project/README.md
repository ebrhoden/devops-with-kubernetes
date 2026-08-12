# Todo App

## Overview

This project consists of two FastAPI applications:

* **Todo App** serves the HTML interface, handles random image downloading and caching, and communicates with the Todo Backend.
* **Todo Backend** provides the API for creating and retrieving todos. Todos are currently stored in memory.

The applications communicate over HTTP using Kubernetes Services.

For more details about each application, see:

* [`todo-app/README.md`](todo-app/README.md)
* [`todo-backend/README.md`](todo-backend/README.md)

## Deploy the application

Apply all Kubernetes manifests:

```bash
kubectl apply -f manifests/
```

Apply the storage (need for Todo App):
```bash
kubectl apply -f storage/
```

Verify that the Pods are running:

```bash
kubectl get pods
```

Verify the Services:

```bash
kubectl get svc
```

Verify the Ingress:

```bash
kubectl get ingress
```

## Test the application

If using the provided Ingress, open:

```text
http://localhost:8081/
```

The page should display the Todo App with the configured message, a random image, and the current todo items.

### Create a todo

Enter a new todo in the form and click **Send**.

The new todo should appear in the list after the page reloads.

### Verify the backend

You can also test the Todo Backend directly from inside the Todo App Pod:

```bash
kubectl exec -it deploy/todoapp-dep -- \
  wget -qO- http://todo-backend:8000/todos
```

The command should return the current list of todos.

### Verify the complete flow

To test the communication between the applications:

1. Open `http://localhost:8081/`.
2. Confirm that the existing todos are displayed.
3. Create a new todo using the form.
4. Confirm that the new todo appears in the browser.
5. Run the command above to verify that the Todo Backend contains the new todo.

The Todo App is exposed through the Ingress, while the Todo Backend is accessed internally through its Kubernetes Service.
