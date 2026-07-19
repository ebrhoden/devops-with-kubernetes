# Todo App

## Source Code

The `Dockerfile` and `app.py` files are the source code for the Docker image `ebrhoden/todo_app:0.0.4`.

The rendered page shows a cached image, 3 hardcoded TODOs, an input field and a button. Both the input field and the button are not fully functional yet.

## Testing the Image Cache

The application downloads a random image from Lorem Picsum and caches it in a PersistentVolume. The cached image is reused until it expires (10 minutes in production, or the value configured by the `CACHE_SECONDS` environment variable).

For development, `CACHE_SECONDS` is set to `20` seconds to make testing easier.

## Deploy the application

Apply the Kubernetes storage manifests:
```bash
kubectl apply -f storage/
```

Apply the Kubernetes manifests:

```bash
kubectl apply -f manifests/
```

Verify that the pod is running:

```bash
kubectl get pods
```

## Access the application

Port-forward the Service:

```bash
kubectl port-forward svc/todoapp-svc 8000:2345
```

Then open:

```
http://localhost:8000/
```

## Verify image caching

1. Open the application. A random image should be displayed.
2. Refresh the page several times within 20 seconds. The same image should be displayed each time.
3. Wait more than 20 seconds.
4. Refresh the page again. A new random image should now be downloaded and displayed.

## Verify persistence

To verify that the image is stored in the PersistentVolume:

1. Load the application once so the image is downloaded.
2. Delete the running pod:

```bash
kubectl delete pod -l app=todoapp
```

3. Wait for Kubernetes to create a replacement pod:

```bash
kubectl get pods
```

4. Refresh the application before the cache expires.

The same image should still be displayed, demonstrating that the cached image was restored from the PersistentVolume rather than downloaded again.

## Verify the cached files

To inspect the cached files inside the container:

```bash
kubectl exec -it deploy/todoapp-dep -- ls -l /data
```

The cache directory should contain the downloaded image (and any metadata file if your implementation uses one).