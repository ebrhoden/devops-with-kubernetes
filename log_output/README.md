# Log Output with declarative deployment

## Source Code

The `Dockerfile` and `random_logger.py` files are the source code for the Docker image `ebrhoden/log_output:0.0.3`.

## Creating the cluster with open ports on server node and agent node

To create a cluster granting access to server node on port 8081 and to one of the agent nodes on port 8082, run the following command:
```bash
k3d cluster create --port 8082:30000@agent:0 -p 8081:80@loadbalancer --agents 2
```

## Deployment to Kubernetes

To deploy this image to Kubernetes, run the following command:

```bash
kubectl apply -f manifests
```

## Checks

To check the behavior, access ```localhost:8081``` and check the status (timestamp + random message).