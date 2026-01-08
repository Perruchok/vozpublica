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

# Run scraping - whole transcripts
scrape-whole:
	nohup ./venv/bin/python backend/ingestion/extract_whole_main.py 2>&1 | tee -a scraper.log &

# Run scraping - metadata only
scrape-meta:
	./venv/bin/python backend/ingestion/extract_meta_main.py

# Help - show available commands
help:
	@echo "Available commands:"
	@echo "  make run-backend      - Start FastAPI backend (port 8000)"
	@echo "  make run-frontend     - Start Next.js frontend in dev mode (port 3000)"
	@echo "  make start-frontend   - Start Next.js frontend in production mode"
	@echo "  make run-all          - Start both backend and frontend"
	@echo "  make scrape-whole     - Run whole transcript scraping"
	@echo "  make scrape-meta      - Run metadata scraping"
	@echo "  make help             - Show this help message"