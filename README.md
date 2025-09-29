# Improvise Python App (GitHub Copilot exercise)

Repository name: `01-improvise-python-app-copilot`.

## What this project contains
  
  - `main.py` — FastAPI app with endpoints:

  - `GET /` — welcome message

  - `POST /checksum` — accepts JSON `{"text": "..."}` and returns MD5 checksum

  - `POST /tokens` — accepts JSON `{"text": "..."}` and returns 5 pseudorandom tokens and checksum

  - `GET /form` — interactive HTML form that calls `/tokens` and displays results

  - `templates/form.html` — interactive form page

  - `tests/test_main.py` — pytest test cases

  - `requirements.txt` — Python dependencies

## Run locally (or in Codespaces)

1. Create and activate virtual environment (optional):

python -m venv .venv

source .venv/bin/activate   # macOS / Linux
   
.venv\Scripts\activate      # Windows

2.Install dependencies:

pip install -r requirements.txt

3.Start the app with uvicorn:

uvicorn main:app --reload --host 0.0.0.0 --port 8000

4. Visit:

Interactive form: http://localhost:8000/form

Swagger UI / OpenAPI: http://localhost:8000/docs

Redoc: http://localhost:8000/redoc

# Run Locally #

pytest -q


