# ComicCraft AI

ComicCraft is an AI-powered comic story creator.

## Technologies

- Python
- FastAPI
- Gemini
- Hugging Face
- Jinja2
- Pillow
- FPDF

## Project Flow

User Story
↓
Gemini Outline
↓
Five Comic Panels
↓
Comic Story
↓
Image Generation
↓
Comic Preview
↓
PDF Export

## Installation

Create virtual environment:

python -m venv .venv

Activate:

.venv\Scripts\Activate.ps1

Install packages:

pip install -r requirements.txt

## Configuration

Create a `.env` file:

USE_MOCK_AI=true

## Run

Start the application:

uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000

## API Documentation

http://127.0.0.1:8000/docs

## Health Check

http://127.0.0.1:8000/health

## Smoke Test

Run:

python smoke_test.py

Expected:

ComicCraft smoke test PASSED