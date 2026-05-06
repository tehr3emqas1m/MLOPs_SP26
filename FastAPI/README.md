
# FastAPI Tutorial

<img width="1024" height="369" alt="logo-teal" src="https://github.com/user-attachments/assets/b6fe672e-e113-4ffd-bede-6e094a569be9" />

---

FastAPI is a modern Python web framework for building high-performance APIs (especially for ML model serving) with automatic documentation and data validation.

- Built on top of **Starlette** — manages how the API receives requests and responds to them (HTTP requests/responses, routing, WebSockets, middleware)
- Built on top of **Pydantic** — validates and parses request data (ensures correct types/formats)

## Why Do We Need an API?

```
Frontend ──→ HTTP Request (with JSON) ──→ API Endpoint ──→ Backend
                                                              ↓
Frontend ←── HTTP Response (with JSON) ←── API Endpoint ←─────┘
```

An endpoint in FastAPI is a URL path (e.g., `/students`) tied to an HTTP method.

---

## How FastAPI Works

```
Client
   ↓
Uvicorn (ASGI server)
   ↓
FastAPI (framework)
   ↓
   ├── Starlette (handles routing, requests, responses)
   └── Pydantic (handles data validation)
```

---

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv myenv
source myenv/bin/activate   # macOS/Linux
myenv\Scripts\activate      # Windows
```

Install required libraries:

```bash
pip install fastapi uvicorn pydantic
```

---

## Hello World Example

Create the file:

```bash
touch helloworld.py
```

```python
from fastapi import FastAPI

app = FastAPI(title="Hello World App")

# GET request — used to fetch something from a server
@app.get("/")
def hello():
    return {"message": "Hello world!"}

@app.get("/mlops")
def mlops():
    return {"message": "In this course we study MLOps"}
```

Run the server:

```bash
uvicorn helloworld:app --reload
```

Uvicorn will start and listen for HTTP requests.

---

## HTTP Methods

```
CRUD    →   HTTP Verb
Create  →   POST
Read    →   GET
Update  →   PUT / PATCH
Delete  →   DELETE
```

