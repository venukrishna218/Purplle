import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("emitter")

API_URL = "http://localhost:8000/events/ingest"

def emit_events(events_batch: list):
    """Pushes a batch of tracked events to the FastAPI backend."""
    if not events_batch:
        return
        
    try:
        response = requests.post(API_URL, json=events_batch, timeout=2)
        if response.status_code == 202:
            logger.info(f"Successfully emitted {len(events_batch)} events.")
        else:
            logger.error(f"API Error: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to reach API: {e}. Is it running?")