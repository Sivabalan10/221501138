# URL Shortener Service

A simple URL shortening service built with Flask, SQLite, and logging middleware.  
This project demonstrates REST API design, error logging, and basic analytics for shortened URLs.

---
Docs reference link - `https://docs.google.com/document/d/1sew1l6fuzaAQ36Avv6G4eczMAGk4Qcyj8gN9HG1I_LQ/edit?usp=sharing`
## Features

- **Shorten URLs** with optional custom shortcode and validity (default: 30 minutes)
- **Redirection** from short URL to original long URL
- **Statistics** for each short URL: clicks, click time, expiry, created time, and source IP
- **Centralized error logging** using a remote logging service (see [Logging Handler](#logging-handler))
- **SQLite** as the database backend

---

## API Endpoints

### 1. Shorten URL

**POST** `/shorturls`

**Request Body:**
```json
{
  "url": "https://example.com",
  "validity": 30,         // (optional, in minutes, default: 30)
  "shortcode": "custom"   // (optional)
}
```

**Response:**
```json
{
  "shortLink": "http://localhost:5000/r/abc123",
  "expiry": "2024-07-05T12:34:56.789Z"
}
```

---

### 2. Get Short URL Statistics

**GET** `/shorturl/<short_url_link>`

**Response:**
```json
{
  "created_time": "...",
  "longurl": "...",
  "shorturl": "...",
  "validity": 30,
  "expiry": "...",
  "clicks": [
    {
      "url": "...",
      "time": "...",
      "source": "IP"
    }
  ]
}
```

---

### 3. Redirect to Long URL

**GET** `/r/<shortcode>`

Redirects to the original long URL.

---

## Logging Handler

This project includes a centralized logging handler (`handler.py`) that sends error and debug logs to a remote logging service.  
The handler uses the `requests` library to POST logs to `http://20.244.56.144/evaluation-service/logs` with the following structure:

```json
{
  "stack": "backend",
  "level": "error",
  "package": "route",
  "message": "Error message"
}
```

- The log function is called as `log(message, level, package, stack)` throughout the codebase.
- The Bearer token for authorization is stored in the `.env` file as `LOG_AUTH_TOKEN`.
- All errors, including invalid URLs, missing parameters, and database issues, are logged using this handler.
.

---

## Installation Guide

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# source venv/bin/activate  # On Linux/Mac
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:
```bash
pip install flask flask-cors python-dotenv validators requests
```

### 4. Set up environment variables

Create a `.env` file in your project root:
```
LOG_AUTH_TOKEN=your_token_here
```
(Use the provided token from your `.env`)

### 5. Run the application

```bash
python backend/route.py
```

The API will be available at `http://localhost:5000/`

---

## Database

- SQLite database file is created automatically (`urlshortener.db`).
- No manual setup required.

---

