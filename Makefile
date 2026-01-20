# Run the backend (FastAPI with venv)
run-backend:
	./venv/bin/uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

# Run the frontend (Next.js in dev mode - no venv needed, uses npm)
run-frontend:
	cd frontend && npm run dev

# Run the frontend (Next.js in production mode)
start-frontend:
	cd frontend && npm run build && npm start

# Run both services (in background)
run-all:
	@echo "Starting backend..."
	./venv/bin/uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload &
	@echo "Starting frontend..."
	cd frontend && npm run dev

# Run scraping - whole transcripts with Playwright
scrape-whole:
	nohup ./venv/bin/python -m backend.ingestion.extract_whole_main 2>&1 | tee -a scraper.log &

# Run scraping - metadata with Playwright
scrape-meta:
	./venv/bin/python -m backend.ingestion.extract_meta_main

# ============================================
# Docker Commands
# ============================================

# Docker Hub configuration - Best practices for CI/CD
DOCKER_USERNAME ?= ahperru
DOCKER_REPO ?= vozpublica-backend
DOCKER_IMAGE = $(DOCKER_USERNAME)/$(DOCKER_REPO)
VERSION ?= $(shell git describe --tags --always 2>/dev/null || echo "latest")
GIT_SHA ?= $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")
BRANCH ?= $(shell git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

# Build Docker image for testing
docker-build:
	@echo "Building Docker image..."
	docker build -t vozpublica-backend:test .
	@echo "✅ Docker image built successfully: vozpublica-backend:test"

# Build and push to Docker Hub with best practices
docker-publish:
	@echo "Publishing to Docker Hub (CI/CD Best Practices)..."
	@echo "  Repository: $(DOCKER_IMAGE)"
	@echo "  Version: $(VERSION)"
	@echo "  Git SHA: $(GIT_SHA)"
	@echo "  Branch: $(BRANCH)"
	@echo ""
	@if [ -z "$(DOCKER_USERNAME)" ]; then \
		echo "❌ Error: DOCKER_USERNAME not set."; \
		exit 1; \
	fi
	@echo "🔐 Make sure you are logged in to Docker Hub:"
	@echo "   docker login"
	@echo ""
	@echo "Building image with multiple tags..."
	docker build \
		-t $(DOCKER_IMAGE):$(VERSION) \
		-t $(DOCKER_IMAGE):latest \
		-t $(DOCKER_IMAGE):$(BRANCH) \
		-t $(DOCKER_IMAGE):sha-$(GIT_SHA) \
		.
	@echo "✅ Image built with tags: $(VERSION), latest, $(BRANCH), sha-$(GIT_SHA)"
	@echo ""
	@echo "🚀 Pushing to Docker Hub..."
	@echo ""
	@echo "  Pushing $(DOCKER_IMAGE):$(VERSION)..."
	docker push $(DOCKER_IMAGE):$(VERSION)
	@echo "  Pushing $(DOCKER_IMAGE):latest..."
	docker push $(DOCKER_IMAGE):latest
	@echo "  Pushing $(DOCKER_IMAGE):$(BRANCH)..."
	docker push $(DOCKER_IMAGE):$(BRANCH)
	@echo "  Pushing $(DOCKER_IMAGE):sha-$(GIT_SHA)..."
	docker push $(DOCKER_IMAGE):sha-$(GIT_SHA)
	@echo ""
	@echo "✅ Successfully published to Docker Hub!"
	@echo ""
	@echo "Repository: https://hub.docker.com/r/$(DOCKER_IMAGE)"
	@echo ""
	@echo "Available tags:"
	@echo "  - $(DOCKER_IMAGE):$(VERSION)       (Version tag)"
	@echo "  - $(DOCKER_IMAGE):latest           (Latest release)"
	@echo "  - $(DOCKER_IMAGE):$(BRANCH)        (Branch tag)"
	@echo "  - $(DOCKER_IMAGE):sha-$(GIT_SHA)   (Commit hash)"
	@echo ""
	@echo "To pull: docker pull $(DOCKER_IMAGE):$(VERSION)"

# Login to Docker Hub
docker-login:
	@echo "Logging in to Docker Hub..."
	docker login -u $(DOCKER_USERNAME)
	@echo "✅ Logged in successfully"

# View published images on Docker Hub
docker-info:
	@echo "Docker Hub Configuration (CI/CD Best Practices)"
	@echo "=================================================="
	@echo "  Username: $(DOCKER_USERNAME)"
	@echo "  Repository: $(DOCKER_REPO)"
	@echo "  Full Image: $(DOCKER_IMAGE)"
	@echo ""
	@echo "Version Information:"
	@echo "  Version Tag: $(VERSION)"
	@echo "  Git SHA: $(GIT_SHA)"
	@echo "  Branch: $(BRANCH)"
	@echo ""
	@echo "Docker Hub URL:"
	@echo "  https://hub.docker.com/r/$(DOCKER_IMAGE)"
	@echo ""
	@echo "Tags that will be created:"
	@echo "  - $(DOCKER_IMAGE):$(VERSION)       (Semantic version)"
	@echo "  - $(DOCKER_IMAGE):latest           (Latest production)"
	@echo "  - $(DOCKER_IMAGE):$(BRANCH)        (Branch tag)"
	@echo "  - $(DOCKER_IMAGE):sha-$(GIT_SHA)   (Git commit)"
	@echo ""
	@echo "To override variables:"
	@echo "  make docker-publish DOCKER_USERNAME=ahperru VERSION=v1.1.0"

# Run Docker container with environment variables from .env file
docker-run:
	@echo "Starting Docker container..."
	@if [ ! -f .env ]; then \
		echo "❌ Error: .env file not found. Please create one with your configuration."; \
		exit 1; \
	fi
	docker run -d \
		-p 8000:8000 \
		--name vozpublica-test \
		--env-file .env \
		vozpublica-backend:test
	@echo "✅ Container started: vozpublica-test"
	@echo "   Access at: http://localhost:8000"
	@echo "   Check logs: make docker-logs"

# Test Docker container health
docker-test:
	@echo "Testing Docker container health..."
	@sleep 5
	@if curl -f -s http://localhost:8000/health > /dev/null; then \
		echo "✅ Health check passed!"; \
		curl -s http://localhost:8000/health | python -m json.tool; \
	else \
		echo "❌ Health check failed. Check logs with: make docker-logs"; \
		exit 1; \
	fi

# View Docker container logs
docker-logs:
	docker logs -f vozpublica-test

# Stop Docker container
docker-stop:
	@echo "Stopping Docker container..."
	docker stop vozpublica-test || true
	@echo "✅ Container stopped"

# Remove Docker container
docker-clean:
	@echo "Cleaning up Docker resources..."
	docker stop vozpublica-test 2>/dev/null || true
	docker rm vozpublica-test 2>/dev/null || true
	@echo "✅ Container removed"

# Remove Docker image
docker-remove-image:
	@echo "Removing Docker image..."
	docker rmi vozpublica-backend:test || true
	@echo "✅ Image removed"

# Full Docker test cycle: build → run → test → cleanup
docker-test-full:
	@echo "Running full Docker test cycle..."
	@make docker-clean || true
	@make docker-build
	@make docker-run
	@echo "Waiting for container to start..."
	@sleep 10
	@make docker-test
	@echo ""
	@echo "✅ Full Docker test completed successfully!"
	@echo "   Container is running at: http://localhost:8000"
	@echo "   To stop: make docker-stop"
	@echo "   To cleanup: make docker-clean"

# Shell into running container for debugging
docker-shell:
	docker exec -it vozpublica-test /bin/bash

# Help - show available commands
help:
	@echo "Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  make run-backend                - Start FastAPI backend (port 8000)"
	@echo "  make run-frontend               - Start Next.js frontend in dev mode (port 3000)"
	@echo "  make start-frontend             - Start Next.js frontend in production mode"
	@echo "  make run-all                    - Start both backend and frontend"
	@echo ""
	@echo "Data Scraping:"
	@echo "  make scrape-meta                - Run metadata scraping"
	@echo "  make scrape-whole               - Run full transcript scraping"
	@echo ""
	@echo "Docker (Testing):"
	@echo "  make docker-build               - Build Docker image locally"
	@echo "  make docker-run                 - Run Docker container (requires .env file)"
	@echo "  make docker-test                - Test Docker container health"
	@echo "  make docker-test-full           - Full test cycle (build+run+test)"
	@echo "  make docker-logs                - View container logs"
	@echo "  make docker-shell               - Open shell in running container"
	@echo "  make docker-stop                - Stop Docker container"
	@echo "  make docker-clean               - Stop and remove container"
	@echo "  make docker-remove-image        - Remove Docker image"
	@echo ""
	@echo "Docker Hub (Publishing):"
	@echo "  make docker-login               - Login to Docker Hub"
	@echo "  make docker-publish             - Build and push to Docker Hub"
	@echo "  make docker-info                - Show Docker Hub configuration"
	@echo ""
	@echo "  make help                       - Show this help message"