# Todo App

## Source Code

This project consists of a FastAPI application that serves the browser-facing Todo application.

The application is responsible for:

* Serving the HTML interface.
* Retrieving todos from the Todo Backend.
* Sending new todos to the Todo Backend.
* Downloading random images from `picsum.photos`.
* Caching the downloaded image using a PersistentVolume.
* Serving the cached image through `/image`.

The application does not store the todo items itself. Todo data is managed by the Todo Backend.

The application is packaged as the following Docker image:

* `ebrhoden/todo_app:0.0.5`

## Application Architecture

The Todo App is the browser-facing application.

When the browser requests `/`, Todo App retrieves the todos from the Todo Backend over HTTP and renders them in the HTML page.

When a new todo is submitted, Todo App sends the todo to the Todo Backend.

The random image functionality remains inside Todo App.

## Configuration

Todo App uses the following environment variables:

```text
MESSAGE
CACHE_SECONDS
BACKEND_URL
```

For example:

```yaml
env:
  - name: MESSAGE
    value: "This is a message from the environment variable. An image should be displayed below."

  - name: CACHE_SECONDS
    value: "20"

  - name: BACKEND_URL
    value: "http://todo-backend:8000"
```

`BACKEND_URL` points to the Kubernetes Service used to communicate with the Todo Backend.

## Deploy the application

Apply the PersistentVolume and PersistentVolumeClaim:

```bash
kubectl apply -f persistentvolume.yaml
kubectl apply -f persistentvolumeclaim.yaml
```

Apply the Deployment, Service, and Ingress:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

Verify that the Pod is running:

```bash
kubectl get pods
```

Verify that the Service was created:

```bash
kubectl get svc
```

Verify that the Ingress was created:

```bash
kubectl get ingress
```

## Access the application

If using the provided Ingress, open:

```text
http://localhost:8081/
```

The page should display:

* The configured message.
* A random image.
* The current todo items.
* A form for creating new todos.

## Create a todo

Enter a todo in the form and click **Send**.

Todo App sends the todo to the Todo Backend:

```text
POST http://todo-backend:8000/todos
```

After the request succeeds, the browser is redirected back to `/`.

Todo App then retrieves the updated list:

```text
GET http://todo-backend:8000/todos
```

The newly created todo should appear in the browser.

## Verify HTTP communication

Open:

```text
http://localhost:8081/
```

Create a new todo, for example:

```text
Learn Kubernetes Services
```

The new todo should appear in the list.

This demonstrates that Todo App is communicating with Todo Backend over HTTP rather than storing the todos itself.

## Verify pod-to-pod communication

To verify that Todo App can reach the Todo Backend from inside the cluster:

```bash
kubectl exec -it deploy/todoapp-dep -- \
  wget -qO- http://todo-backend:8000/todos
```

(or use `curl` if available).

The command should return the current list of todos.

## Verify the deployment

List the running resources:

```bash
kubectl get deployments
kubectl get services
kubectl get ingress
kubectl get pods
```

The Todo App should be running behind the `todoapp-svc` Service and exposed through the Ingress.

The Todo App should also be able to communicate with the `todo-backend` Service from inside the Kubernetes cluster.
