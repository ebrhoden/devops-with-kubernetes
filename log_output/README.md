# Log Output

## Source Code

The `Dockerfile` and `random_logger.py` files are the source code for the Docker image `ebrhoden/log_output:0.0.2`.

## Deployment to Kubernetes

To deploy this image to Kubernetes, run the following command:

```bash
kubectl create deployment todoapp-dep --image=ebrhoden/log_output:0.0.2
```
