.PHONY: help dev dev-down dev-logs dev-clean infra-init infra-plan infra-apply infra-destroy migrate migrate-create test lint format backend-shell frontend-shell

# Default target
help:
	@echo "AI Website Builder - Makefile Commands"
	@echo ""
	@echo "Development:"
	@echo "  make dev           - Start all services with docker-compose"
	@echo "  make dev-down      - Stop all services"
	@echo "  make dev-logs      - Show logs from all services"
	@echo "  make dev-clean     - Remove all containers, volumes, and images"
	@echo ""
	@echo "Infrastructure:"
	@echo "  make infra-init    - Initialize Terraform"
	@echo "  make infra-plan    - Plan Terraform changes"
	@echo "  make infra-apply   - Apply Terraform changes"
	@echo "  make infra-destroy - Destroy Terraform infrastructure"
	@echo ""
	@echo "Database:"
	@echo "  make migrate        - Run database migrations"
	@echo "  make migrate-create - Create a new migration"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test          - Run all tests"
	@echo "  make lint          - Run linters"
	@echo "  make format        - Format code"
	@echo ""
	@echo "Utils:"
	@echo "  make backend-shell  - Open shell in backend container"
	@echo "  make frontend-shell - Open shell in frontend container"

# Development
dev:
	@echo "Starting development environment..."
	docker-compose up -d
	@echo "Services started. Access:"
	@echo "  - Backend API: http://localhost:8000"
	@echo "  - Frontend: http://localhost:3000"
	@echo "  - API Docs: http://localhost:8000/api/docs"

dev-down:
	@echo "Stopping development environment..."
	docker-compose down

dev-logs:
	docker-compose logs -f

dev-clean:
	@echo "Cleaning up development environment..."
	docker-compose down -v --rmi all --remove-orphans
	@echo "Cleanup complete."

# Infrastructure
infra-init:
	@echo "Initializing Terraform..."
	cd infra && terraform init

infra-plan:
	@echo "Planning Terraform changes..."
	cd infra && terraform plan -out=tfplan

infra-apply:
	@echo "Applying Terraform changes..."
	@echo "WARNING: This will create/modify AWS resources."
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ] || exit 1
	cd infra && terraform apply tfplan

infra-destroy:
	@echo "WARNING: This will DESTROY all Terraform-managed infrastructure!"
	@read -p "Are you sure? Type 'yes' to confirm: " confirm && [ "$$confirm" = "yes" ] || exit 1
	cd infra && terraform destroy

# Database migrations
migrate:
	@echo "Running database migrations..."
	docker-compose exec backend alembic upgrade head

migrate-create:
	@read -p "Enter migration name: " name; \
	docker-compose exec backend alembic revision --autogenerate -m "$$name"

# Testing & Quality
test:
	@echo "Running tests..."
	cd backend && pytest -v --cov=app --cov-report=html
	@echo "Coverage report: backend/htmlcov/index.html"

lint:
	@echo "Running linters..."
	cd backend && ruff check .
	cd backend && mypy app
	cd frontend && npm run lint

format:
	@echo "Formatting code..."
	cd backend && black app
	cd backend && ruff check --fix .

# Utils
backend-shell:
	docker-compose exec backend /bin/bash

frontend-shell:
	docker-compose exec frontend /bin/sh

# Setup local AWS resources
setup-local-aws:
	@echo "Setting up local AWS resources in LocalStack..."
	@echo "Creating S3 buckets..."
	aws --endpoint-url=http://localhost:4566 s3 mb s3://ai-wb-sites-local
	aws --endpoint-url=http://localhost:4566 s3 mb s3://ai-wb-assets-local
	aws --endpoint-url=http://localhost:4566 s3 mb s3://ai-wb-templates-local
	@echo "Creating DynamoDB tables..."
	aws --endpoint-url=http://localhost:4566 dynamodb create-table \
		--table-name ai-wb-page-views \
		--attribute-definitions AttributeName=site_id,AttributeType=S AttributeName=timestamp_visitor,AttributeType=S \
		--key-schema AttributeName=site_id,KeyType=HASH AttributeName=timestamp_visitor,KeyType=RANGE \
		--billing-mode PAY_PER_REQUEST
	aws --endpoint-url=http://localhost:4566 dynamodb create-table \
		--table-name ai-wb-page-view-daily \
		--attribute-definitions AttributeName=site_id,AttributeType=S AttributeName=date_page,AttributeType=S \
		--key-schema AttributeName=site_id,KeyType=HASH AttributeName=date_page,KeyType=RANGE \
		--billing-mode PAY_PER_REQUEST
	@echo "Local AWS resources created."
