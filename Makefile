# ============================================
# NEXOVA — Makefile
# ============================================

.DEFAULT_GOAL := help
.PHONY: help dev dev-backend dev-frontend build test lint clean deploy

# ---- Colors ----
CYAN  := \033[36m
RESET := \033[0m

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)%-20s$(RESET) %s\n", $$1, $$2}'

# ---- Development ----

dev: ## Start all services (backend + frontend)
	docker compose up --build

dev-backend: ## Start backend only
	cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8080

dev-frontend: ## Start frontend only
	cd frontend && npm run dev

# ---- Build ----

build: ## Build all Docker images
	docker compose build

build-backend: ## Build backend image
	docker build -t nexova-api ./backend

build-frontend: ## Build frontend image
	docker build -t nexova-web ./frontend

# ---- Testing ----

test: test-backend test-frontend ## Run all tests

test-backend: ## Run backend tests
	cd backend && python -m pytest tests/ -v --cov=. --cov-report=term-missing

test-frontend: ## Run frontend tests
	cd frontend && npm run test

test-e2e: ## Run E2E tests
	cd frontend && npx playwright test

test-a11y: ## Run accessibility tests
	cd frontend && npx playwright test --project=accessibility

# ---- Linting ----

lint: lint-backend lint-frontend ## Lint everything

lint-backend: ## Lint backend
	cd backend && ruff check . && ruff format --check . && mypy .

lint-frontend: ## Lint frontend
	cd frontend && npm run lint && npm run type-check

format: ## Format all code
	cd backend && ruff format .
	cd frontend && npm run format

# ---- Security ----

security-scan: ## Run security scans
	cd backend && bandit -r . -ll -ii
	cd frontend && npm audit

# ---- Infrastructure ----

tf-init: ## Initialize Terraform
	cd infrastructure && terraform init

tf-plan: ## Plan Terraform changes
	cd infrastructure && terraform plan -out=tfplan

tf-apply: ## Apply Terraform changes
	cd infrastructure && terraform apply tfplan

# ---- Deployment ----

deploy: ## Deploy to Cloud Run via Cloud Build
	gcloud builds submit --config=cloudbuild.yaml

deploy-backend: ## Deploy backend only
	cd backend && gcloud run deploy nexova-api \
		--source . \
		--region $(GCP_REGION) \
		--allow-unauthenticated

deploy-frontend: ## Deploy frontend only
	cd frontend && gcloud run deploy nexova-web \
		--source . \
		--region $(GCP_REGION) \
		--allow-unauthenticated

# ---- Data ----

seed-data: ## Seed Firestore with sample data
	cd backend && python -m simulation.data_generator

# ---- Clean ----

clean: ## Remove build artifacts
	rm -rf backend/__pycache__ backend/.pytest_cache backend/.mypy_cache backend/.ruff_cache
	rm -rf frontend/.next frontend/node_modules frontend/coverage
	docker compose down --volumes --remove-orphans
