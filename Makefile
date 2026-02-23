.PHONY: help install dev test lint format migrate shell clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies
	pip install -r backend/requirements-dev.txt
	cd frontend && npm install

dev: ## Start development servers
	docker-compose up

test: ## Run backend tests
	cd backend && pytest

lint: ## Run linters
	cd backend && flake8 .
	cd frontend && npm run lint

format: ## Format code
	cd backend && black . && isort .
	cd frontend && npx prettier --write .

migrate: ## Run Django migrations
	cd backend && python manage.py migrate

shell: ## Open Django shell
	cd backend && python manage.py shell

clean: ## Remove Python cache files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; true
	find . -name "*.pyc" -delete
