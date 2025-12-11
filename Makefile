# Create a command to run the FastAPI application
run:
	uvicorn app.app:app --host 0.0.0.0 --port 8000