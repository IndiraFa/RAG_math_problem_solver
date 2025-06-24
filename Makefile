.PHONY: build up down index backend

# Build all Docker images
build:
	docker-compose build

# Start your FastAPI backend and dependencies
up:
	docker-compose up

# Stop all running containers
down:
	docker-compose down

# Rebuild and start indexing Hugging Face dataset
index:
	docker-compose up --build indexer

# Run just the backend service
backend:
	docker-compose up backend

