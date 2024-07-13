
```markdown
# Ollama Text Generation API

This project implements a simple API wrapper around the Ollama text generation service using Flask, Docker, and Kubernetes. It includes steps for setting up the project, running the application, and performing load testing using k6.

## Technologies Used

- **Flask**: Python web framework for creating the API.
- **Docker**: Containerization platform for packaging the application.
- **Kubernetes**: Container orchestration platform for deploying the application.
- **k6**: Load testing tool to test the API.

## Prerequisites

- Docker installed on your machine.
- Kubernetes installed and configured (Minikube, Kind, or any cloud provider like Civo or Linode).
- k6 installed for load testing.

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/ollama-api.git
cd ollama-api
```




### 2. Build and Run the Docker Container

1. **Build the Docker Image**:

   ```sh
   docker build -t ollama-api .
   ```

2. **Run the Docker Container**:

   ```sh
   docker run -p 5000:5000 ollama-api
   ```

### 3. Deploy to Kubernetes

Create Kubernetes deployment and service manifests:

#### `deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama-api-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ollama-api
  template:
    metadata:
      labels:
        app: ollama-api
    spec:
      containers:
      - name: ollama-api
        image: ollama-api:latest
        ports:
        - containerPort: 5000
```

#### `service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ollama-api-service
spec:
  selector:
    app: ollama-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

Apply the Kubernetes manifests:

```sh
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### 7. Load Testing with k6

#### Install k6

Follow the instructions on the [k6 installation page](https://k6.io/docs/getting-started/installation/).

#### Create a k6 Load Test Script

Create a file named `load_test.js` with the following content:

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 10 },  // ramp up to 10 users over 30 seconds
    { duration: '1m', target: 10 },   // stay at 10 users for 1 minute
    { duration: '30s', target: 0 },   // ramp down to 0 users over 30 seconds
  ],
};

export default function () {
  let url = 'http://localhost:5000/generate';
  let payload = JSON.stringify({ prompt: 'Hello, Ollama!' });
  let params = { headers: { 'Content-Type': 'application/json' } };

  let res = http.post(url, payload, params);
  check(res, {
    'is status 200': (r) => r.status === 200,
    'response time is less than 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}
```

#### Run the k6 Load Test Script

```sh
k6 run load_test.js
```

## Conclusion

This project sets up a simple API wrapper around the Ollama text generation service using Flask, Docker, and Kubernetes, and includes instructions for performing load testing with k6.

Feel free to contribute and improve this project by submitting issues and pull requests. Happy coding!
```

This README file provides a comprehensive guide to setting up, running, and testing the Ollama text generation API. It includes details about the technologies used, step-by-step setup instructions, and commands for running and load testing the application.
