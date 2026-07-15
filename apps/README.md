## Source code
log-reader, log-writter and pingpong folders contain source code for the applications

## Creating the cluster with open ports on server node and agent node

To create a cluster granting access to server node on port 8081 and to one of the agent nodes on port 8082, run the following command:
```bash
k3d cluster create --port 8082:30000@agent:0 -p 8081:80@loadbalancer --agents 2
```

## Deployment to Kubernetes with persistent volume

To deploy this image to Kubernetes, run the following command:

```bash
kubectl apply -f manifests
kubectl apply -f storage
```

## Checks

To check the behavior, access ```localhost:8081/status```