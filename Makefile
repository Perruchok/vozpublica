# Create a command to run the FastAPI application
run:
	./venv/bin/uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

# Run scrapping
scrape whole:
	nohup python extract_whole_main.py 2>&1 | tee -a scraper.log &

scrape meta: 
	python extract_meta_main.py