# main.py
"""
FastAPI app for:
- generating pseudorandom tokens derived from input text
- returning a checksum (MD5) of the input text
- serving an interactive HTML page to call the API
This file includes Pydantic models, endpoint docstrings, and comments for clarity.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import hashlib
import secrets
import os
from typing import List

app = FastAPI(
    title="Improvise Python App (Copilot)",
    description="Demo FastAPI app that generates pseudorandom tokens and checksums. Built with GitHub Copilot.",
    version="1.0.0",
)

# Templates directory (templates/form.html)
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))


# ---------------------------
# Pydantic models
# ---------------------------
class TextOnly(BaseModel):
    """
    Request model for endpoints that accept JSON body: {"text": "..."}
    """
    text: str


class TokensResponse(BaseModel):
    """
    Response model for the /tokens endpoint.
    """
    tokens: List[str]
    checksum: str


# ---------------------------
# Helper functions
# ---------------------------
def _checksum_md5(text: str) -> str:
    """Return the MD5 checksum (hex) of the given text."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def _generate_tokens_from_text(text: str, count: int = 5) -> List[str]:
    """
    Generate `count` pseudorandom tokens derived from the input text.
    Each token = SHA-256(text + '-' + counter + '-' + random salt)
    """
    tokens = []
    for i in range(count):
        salt = secrets.token_hex(8)  # cryptographically strong random salt
        token = hashlib.sha256(f"{text}-{i}-{salt}".encode("utf-8")).hexdigest()
        tokens.append(token)
    return tokens


# ---------------------------
# Routes / Endpoints
# ---------------------------
@app.get("/", summary="Welcome route")
def welcome():
    """
    Simple welcome route.
    Customize `participant_name` variable below with your name.
    """
    participant_name = "mallela sahid"  # <<-- change this to your name (e.g. "Mark")
    return {"message": f"Welcome to the Improvise Python App — built for {participant_name}"}


@app.post("/checksum", response_model=dict, summary="Compute MD5 checksum of provided text")
def checksum_endpoint(body: TextOnly):
    """
    Accepts JSON: {"text": "..."} and returns MD5 checksum:
    Example response: {"text": "...", "checksum": "..." }
    """
    cs = _checksum_md5(body.text)
    return {"text": body.text, "checksum": cs}


@app.post("/tokens", response_model=TokensResponse, summary="Generate list of tokens from text")
def tokens_endpoint(body: TextOnly):
    """
    Accepts JSON: {"text": "..."} and returns:
      - tokens: list of 5 pseudorandom tokens derived from the text
      - checksum: MD5 checksum of the text
    """
    checksum = _checksum_md5(body.text)
    tokens = _generate_tokens_from_text(body.text, count=5)
    return TokensResponse(tokens=tokens, checksum=checksum)


@app.get("/form", response_class=HTMLResponse, summary="Interactive HTML form")
def form_page(request: Request):
    """
    Renders an interactive HTML form (templates/form.html).
    The form uses JavaScript to submit JSON to /tokens and displays the result.
    """
    participant_name = "mallela sahid"  # <<-- change this to your name
    return templates.TemplateResponse("form.html", {"request": request, "participant": participant_name})
