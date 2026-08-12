# Log Output & Ping Pong

## Source Code

This project consists of two FastAPI applications:

- `log_writer.py` periodically writes a timestamp and a random UUID to a shared log file.
- `log_reader.py` exposes the `/status` endpoint, reads the latest log entry, and retrieves the current pong count from the Ping Pong application via an HTTP request.
- `pingpong.py` exposes:
  - `/pingpong` to increment and return the pong counter.
  - `/pings` to return the current pong count without incrementing it.

The applications are packaged as the following Docker images:

- `ebrhoden/log-writter:0.0.2`
- `ebrhoden/log-reader:0.0.3`
- `ebrhoden/pingpong_app:0.0.3`

## Application Architecture

The applications communicate as follows:

```
Browser
   │
   ├── GET /status
   │
   ▼
Log Reader
   │
   ├── GET http://pingpong-svc:2345/pings
   ▼
Ping Pong
```

The Log Reader retrieves the pong count over HTTP using the Kubernetes Service `pingpong-svc`. No shared volume is used to exchange the counter between the applications.

## Deploy the application

Apply the Kubernetes storage manifests (if using a PersistentVolume for the log files and counter):

```bash
kubectl apply -f storage/
```

Apply the Kubernetes manifests:

```bash
kubectl apply -f manifests/
```

Verify that the pods are running:

```bash
kubectl get pods
```

Verify that the Services were created:

```bash
kubectl get svc
```

## Access the application

If using the provided Ingress, open:

```
http://localhost:8081/status
```

and

```
http://localhost:8081/pingpong
```

Alternatively, port-forward the Services:

```bash
kubectl port-forward svc/log-svc 8000:2345
```

Open:

```
http://localhost:8000/status
```

To access the Ping Pong application:

```bash
kubectl port-forward svc/pingpong-svc 8001:2345
```

Open:

```
http://localhost:8001/pingpong
```

## Verify HTTP communication

1. Open:

```
http://localhost:8081/status
```

The response should look similar to:

```
2026-05-18T12:15:17.705Z: 8523ecb1-c716-4cb6-a044-b9e83bb98e43
Ping / Pongs: 0
```

2. Call the Ping Pong endpoint several times:

```
http://localhost:8081/pingpong
```

3. Refresh the `/status` endpoint.

The `Ping / Pongs` value should increase after each request to `/pingpong`, demonstrating that the Log Reader is retrieving the counter from the Ping Pong application over HTTP.

## Verify pod-to-pod communication

To verify that the Log Reader can reach the Ping Pong Service from inside the cluster:

```bash
kubectl exec -it deploy/log-dep -c log-reader -- wget -qO- http://pingpong-svc:2345/pings
```

(or use `curl` if available).

The command should return the current pong count.

## Verify the deployments

List the running resources:

```bash
kubectl get deployments
kubectl get services
kubectl get ingress
kubectl get pods
```

All deployments should be in the `Running` state, and the `/status` endpoint should continue to display an increasing pong count as requests are made to `/pingpong`.