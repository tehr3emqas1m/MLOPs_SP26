# Student Database API

<img width="50%" alt="CRUD diagram" src="https://github.com/user-attachments/assets/3dd8b142-b14a-4774-8c93-3aa337f3ee63" />


A simple REST API built with **FastAPI** and **SQLite** to manage student records.

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — Web framework
- [SQLite](https://www.sqlite.org/) — Lightweight database
- [Uvicorn](https://www.uvicorn.org/) — ASGI server

---

## Setup

Install dependencies:

```bash
pip install fastapi uvicorn
```

Run the server:

```bash
uvicorn main:app --reload
```

The API will be live at `http://127.0.0.1:8000`

> Auto-generated docs available at `http://127.0.0.1:8000/docs`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/students/` | Create a new student |
| `GET` | `/students/{id}` | Get a student by ID |
| `PUT` | `/students/{id}` | Update a student by ID |
| `DELETE` | `/students/{id}` | Delete a student by ID |

---

## Usage

**Create a student**
```bash
curl -X POST "http://127.0.0.1:8000/students/?name=Ali&age=20"
```

**Read a student**
```bash
curl -X GET "http://127.0.0.1:8000/students/1"
```

**Update a student**
```bash
curl -X PUT "http://127.0.0.1:8000/students/1?name=Musa&age=22"
```

**Delete a student**
```bash
curl -X DELETE "http://127.0.0.1:8000/students/2"
```

---

## Database Schema

```
students
├── id    INTEGER  PRIMARY KEY AUTOINCREMENT
├── name  TEXT     NOT NULL
└── age   INTEGER  NOT NULL
```

---

## Project Structure

```
├── main.py        # FastAPI app and endpoints
└── students.db    # SQLite database (auto-created on first run)
```
