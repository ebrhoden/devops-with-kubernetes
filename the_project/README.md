# Todo App

## Source Code

The `Dockerfile` and `app.py` files are the source code for the Docker image `ebrhoden/todo_app:0.0.1`.

## Deployment to Kubernetes

To deploy this image to Kubernetes, run the following command:

```bash
kubectl create deployment todoapp-dep --image=ebrhoden/todo_app:0.0.1
```
