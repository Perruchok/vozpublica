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

# Build Docker image for testing
docker-build:
	@echo "Building Docker image..."
	docker build -t vozpublica-backend:test .
	@echo "✅ Docker image built successfully: vozpublica-backend:test"

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
	@echo "  make help                       - Show this help message"