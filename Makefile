.PHONY: up down logs test helm-lint helm-template helm-install helm-upgrade helm-uninstall

NAMESPACE ?= testwebapp
RELEASE ?= test-app
CHART ?= ./charts/test-app

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

test:
	curl -s http://localhost:8080/healthz
	@echo "Flood test:"
	@for i in $$(seq 1 20); do \
		curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/healthz; \
	done | sort | uniq -c

helm-lint:
	helm lint $(CHART)

helm-template:
	helm template $(RELEASE) $(CHART) --namespace $(NAMESPACE)

helm-install:
	kubectl create namespace $(NAMESPACE) --dry-run=client -o yaml | kubectl apply -f -
	helm upgrade --install $(RELEASE) $(CHART) --namespace $(NAMESPACE)

helm-upgrade:
	helm upgrade --install $(RELEASE) $(CHART) --namespace $(NAMESPACE)

helm-uninstall:
	helm uninstall $(RELEASE) --namespace $(NAMESPACE)