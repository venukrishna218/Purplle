# Apex Store Intelligence: Real-Time CCTV Analytics Pipeline

A full-stack, real-time computer vision and spatial analytics pipeline designed to convert raw CCTV footage into actionable retail metrics, including precise queue counting, automated anomaly detection, and POS transaction correlation.

## System Overview
This project processes raw video feeds using YOLOv8 spatial tracking, emits strictly structured JSON events to a robust FastAPI backend, and visualizes live store health and conversion funnels via a Streamlit dashboard. 

## Repository Structure
* `/app` - FastAPI intelligence backend, Pydantic data models, and business logic.
* `/pipeline` - YOLOv8 detection engine, OpenCV spatial logic, and network emitter.
* `/docs` - Architectural design and engineering trade-off documentation.
* `/tests` - Pytest suite with edge-case validation.
* `/data` - Directory for raw CCTV `.mp4` files.
* `dashboard.py` - Real-time Streamlit visualization interface.

## Quickstart (Production / Evaluation)
The system is fully containerized for seamless evaluation. To boot the API and database environment, ensure Docker Desktop is running and execute:

```bash
docker compose up --build

Local Development & Testing
To run the full end-to-end system locally with visual tracking:

Install Dependencies:

Bash
pip install -r requirements.txt
Start the Intelligence API (Terminal 1):

Bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Start the Live Dashboard (Terminal 2):

Bash
streamlit run dashboard.py
Run the Vision Pipeline (Terminal 3):
Ensure your video clip is in the data/ folder and update the path in pipeline/detect.py, then run:

Bash
python pipeline/detect.py