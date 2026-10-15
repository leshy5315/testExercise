# testExercise

A small Flask web app that can be run locally with Docker Compose or deployed to Kubernetes with Helm.

- `/` is an HTML status page that shows the environment and which pod served the request.
- `/healthz` is a JSON health check: `{"status": "ok", "service": "app", "env": "..."}`.

## Requirements

- Docker with Compose, for running locally.
- A Kubernetes cluster with `kubectl`, `helm`, [ingress-nginx](https://kubernetes.github.io/ingress-nginx/) and [cert-manager](https://cert-manager.io/), for the Helm deployment.

## Docker Compose

The app runs behind an nginx proxy on `http://localhost:8080` (rate limit: 10 req/s).

| Command     | Description                           |
|-------------|---------------------------------------|
| `make up`   | Build and start the containers        |
| `make down` | Stop the containers and remove volumes |
| `make logs` | Follow the logs                       |
| `make test` | Run a health check and a flood test   |

## Helm (Kubernetes)

The app is deployed to the `testwebapp` namespace with an Ingress and a TLS certificate from cert-manager.

| Command               | Description              |
|-----------------------|--------------------------|
| `make helm-install`   | Create the namespace and install the app |
| `make helm-upgrade`   | Apply chart changes      |
| `make helm-uninstall` | Remove the app           |

Settings are in [`charts/test-app/values.yaml`](charts/test-app/values.yaml):

- `ingress.hosts`, `ingress.tls` and `certificate.dnsNames`: the domain name.
- `certificate.issuer`: which certificate to issue.
  - `letsencrypt`: a browser-trusted certificate. It needs a public domain and open port 80.
  - `selfsigned`: works anywhere, including `localhost`, but the browser shows a warning.
- `letsencrypt.email`: the contact email for Let's Encrypt.
- `image`, `replicaCount`, `env`: the app image, number of replicas and environment variables.

Check the deployment:

```bash
curl https://<your-domain>/healthz       # add -k for selfsigned
```

## CI/CD

[GitHub Actions](.github/workflows/deploy.yml) builds the image on every push and pull request. Pushes also publish it to Docker Hub as `leshy5315/test_webapp:<commit-sha>`. Pushes to `main` additionally tag it `latest` and deploy it with `helm upgrade` over SSH.

The workflow needs these repository secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` (Read & Write), `SSH_HOST` and `SSH_PRIVATE_KEY`.
