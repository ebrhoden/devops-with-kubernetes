# Todo App

## Source Code

The `Dockerfile` and `app.py` files are the source code for the Docker image `ebrhoden/todo_app:0.0.2`.

## Deployment to Kubernetes

To deploy this image to Kubernetes, run the following command:

```bash
kubectl apply -f manifests/deployment.yaml
```

## Checks

To check the behavior, run the following command:
```bash
kubectl port-forward $POD_NAME $DESIRED_PORT:8000
```
And then access ```localhost:$DESIRED_PORT``` and check the greeting message.