# AI Email Triage API

A FastAPI microservice that connects to a Gmail inbox via IMAP and uses Google Gemini (`gemini-2.5-flash`) with strict Pydantic structured outputs to classify, prioritize, summarize, and draft replies for incoming emails.

## Features

* **Strict Structured Outputs (Pydantic):** Enforces a validated JSON schema (`EmailTriageResult`) using Gemini's `response_schema`, eliminating brittle regex parsing and unstructured LLM text.
* **FastAPI REST Backend:** Exposes production-ready endpoints for single-email classification, batch triage, and live inbox processing with automatic Swagger UI (`/docs`).
* **Live Gmail IMAP Ingestion:** Connects securely over SSL (`imap.gmail.com:993`) in `readonly=True` mode to fetch and parse MIME multipart emails without altering unread status.
* **Priority-First Sorting:** Automatically ranks triaged emails from Priority `5` (Urgent) down to `1` (Low/Ignore) and generates draft replies only when `requires_reply` is `true`.

## How It Works

```
Gmail Inbox (IMAP SSL)
        │
        ▼
email_fetcher.py  ──►  Parses MIME headers & plain-text body (EmailInput)
        │
        ▼
classifier.py     ──►  Gemini 2.5 Flash + Pydantic Constrained Decoding
        │
        ▼
main.py (FastAPI) ──►  Validates, sorts by priority_score, returns JSON
```

## Project Structure

```
ai-email-triage-api/
├── schemas.py        # Pydantic data contracts (EmailInput, EmailTriageResult)
├── classifier.py     # Gemini API client with structured JSON output
├── email_fetcher.py  # Built-in IMAP SSL connector & MIME parser
├── main.py           # FastAPI application and REST endpoints
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Verifies server status and active Gemini model. |
| `POST` | `/classify` | Classifies a single email JSON payload. |
| `POST` | `/classify-batch` | Classifies a list of emails in one request. |
| `GET` | `/triage-inbox?limit=5` | Fetches latest emails from Gmail via IMAP, classifies them, and returns them sorted by priority. |

### Sample Response (`POST /classify`)

```
{
  "category": "Billing",
  "priority_score": 5,
  "requires_reply": true,
  "summary": "Production server payment failed and service will be suspended in 12 hours unless updated.",
  "suggested_reply": "Thank you for the alert. We are updating our payment method right away to prevent any service interruption."
}
```

## Setup & Run

### 1. Install Dependencies

```
pip install google-genai pydantic "fastapi[standard]"
```

### 2. Set Environment Variables

Generate a Gemini API key from Google AI Studio and a 16-character Gmail App Password (requires 2-Step Verification).

**Windows (PowerShell):**
```
$env:GEMINI_API_KEY="your_gemini_api_key"
$env:EMAIL_USER="your_email@gmail.com"
$env:EMAIL_APP_PASSWORD="your_16_char_app_password"
```

**Linux / macOS:**
```
export GEMINI_API_KEY="your_gemini_api_key"
export EMAIL_USER="your_email@gmail.com"
export EMAIL_APP_PASSWORD="your_16_char_app_password"
```

### 3. Start the Server

```
python -m fastapi dev main.py
```

Open **`http://127.0.0.1:8000/docs`** in your browser to test all endpoints interactively via Swagger UI.

## Tech Stack

* **Backend:** Python, FastAPI, Uvicorn
* **AI / LLM:** Google GenAI SDK (`gemini-2.5-flash`)
* **Validation:** Pydantic v2
* **Email Ingestion:** Python `imaplib` & `email` (MIME parser)
