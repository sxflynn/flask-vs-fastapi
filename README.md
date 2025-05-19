# Flask vs FastAPI: Async vs Sync Demo

This minimal project demonstrates the performance difference between a sync Flask app and an async FastAPI app using a fake 2-second I/O task (`sleep`).

### Create virtual environment

```shell
python3 -m venv .venv
```

### Active venv

```shell
source .venv/bin/activate
```

### Install packages

```shell
pip install -r requirements.txt
```

### Deactive venv

```shell
deactivate
```

### Recommended: Use Docker Compose

```shell
docker compose up --build
```

### Run the Flask app dev server

```shell
python flask_app.py
```

The Flask server will start on http://localhost:5050

### Run the FastAPI app server (production-ready)

```shell
uvicorn fastapi_app:app --host 0.0.0.0 --port 8000
```

### Run the Flask production server

```shell
gunicorn -w 4 -b 0.0.0.0:5050 wsgi:app
```

## Load testing

To compare how each app handles multiple simultaneous requests, use the load test script.

Flask:

```shell
python load_test.py --url http://localhost:8080/process --requests 500 --concurrency 20
```

FastAPI:

```shell
python load_test.py --url http://localhost:8081/process --requests 500 --concurrency 20
```

Flask Async:

```shell
python load_test.py --url http://localhost:8082/process --requests 500 --concurrency 20
```

