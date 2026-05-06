
# Student Database API with Pydantic Validation

A REST API built with **FastAPI** and **SQLite** that demonstrates data validation using **Pydantic**.

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — Web framework
- [SQLite](https://www.sqlite.org/) — Lightweight database
- [Pydantic](https://docs.pydantic.dev/) — Data validation
- [Uvicorn](https://www.uvicorn.org/) — ASGI server

---

## Setup

Install dependencies:

```bash
pip install fastapi uvicorn pydantic
```

Run the server:

```bash
uvicorn student_CRUD_pydantic:app --reload
```

The API will be live at `http://127.0.0.1:8000`

> Auto-generated docs available at `http://127.0.0.1:8000/docs`

---

## What is Pydantic?

<img width="640" height="162" alt="ceed5147-356e-4c6c-84ee-a550bbf947a6_640x162" src="https://github.com/user-attachments/assets/d92ac938-ab10-43db-b9e6-3a221912370d" />

Python is **dynamically typed** — it does not enforce types at runtime by default.

```python
def myFunc(a, b: int):
    print(f"The sum of integers {a} and {b} is {a+b}")

myFunc(2.8, 3)
# Output: The sum of integers 2.8 and 3 is 5.8  No error — even though 2.8 is a float!
```

Even though `b` is annotated as `int`, Python ignores this at runtime and happily accepts `2.8`. This is a problem when you need to guarantee correct data — especially in APIs.

**Pydantic fixes this** by enforcing types at runtime:

```python
from pydantic import BaseModel

class User(BaseModel):
    a: int
    b: int

def myFunc(user: User):
    print(f"The sum of integers {user.a} and {user.b} is {user.a + user.b}")

obj = User(a=3.6, b=4)  #  Raises ValidationError!
```

```
ValidationError: 1 validation error for User
a
  Input should be a valid integer, got a number with a fractional part
  [type=int_from_float, input_value=3.6, input_type=float]
```

Pydantic **rejects the invalid data immediately** before it can cause bugs deeper in your code.

### How Pydantic Works

```
Define Model → Instantiate with data → Pydantic validates → Use safe object
(BaseModel)     (User(a=3, b=4))       (type checks)        (user.a, user.b)
```

1. **Define a model** — Inherit from `BaseModel` and annotate fields with types
2. **Instantiate with data** — Pass your input to the model constructor
3. **Automatic validation** — Pydantic checks types and raises a clear error on mismatch
4. **Use the validated object** — Access fields as attributes, guaranteed to be correct types

---

## Pydantic in This Project

This project uses four Pydantic models to control what data comes **in** and goes **out** of the API.

| Model | Direction | Required Fields | Used In |
|-------|-----------|-----------------|---------|
| `StudentCreate` | Incoming (request) | `name`, `age` | `POST` |
| `StudentResponse` | Outgoing (response) | `id`, `name`, `age` | `POST`, `GET`, `PATCH` |
| `StudentUpdate` | Incoming (request) | None (all optional) | `PATCH` |
| `MessageResponse` | Outgoing (response) | `detail` | `DELETE` |

### StudentCreate
Validates data when creating a new student.

| Field | Type | Rules |
|-------|------|-------|
| `name` | `str` | Required, 1–100 chars, no whitespace-only, auto-stripped |
| `age` | `int` | Required, must be between 17–25 |

> **Why `@field_validator` for name?**  
> `Field(min_length=1)` alone would accept `"   "` (spaces) as valid since it has length.  
> The validator explicitly rejects strings that are empty after stripping whitespace.

### StudentUpdate
Used for partial updates — all fields are optional so the client can update only what they need.

### StudentResponse
Defines the shape of every student object returned to the client — always includes `id`, `name`, and `age`.

### MessageResponse
Used for simple confirmations like `{"detail": "Student deleted"}`.

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/students/` | Create a new student |
| `GET` | `/students/` | List all students |
| `GET` | `/students/{id}` | Get a student by ID |
| `PATCH` | `/students/{id}` | Partially update a student |
| `DELETE` | `/students/{id}` | Delete a student |

---

## Usage

**Create a student**
```bash
curl -X POST "http://localhost:8000/students/" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "age": 20}'
```

**Get all students**
```bash
curl -X GET "http://localhost:8000/students/"
```

**Get one student by ID**
```bash
curl -X GET "http://localhost:8000/students/1"
```

**Try a non-existent ID**
```bash
curl -X GET "http://localhost:8000/students/999"
```

**Update age only**
```bash
curl -X PATCH "http://localhost:8000/students/1" \
  -H "Content-Type: application/json" \
  -d '{"age": 21}'
```

**Update name only**
```bash
curl -X PATCH "http://localhost:8000/students/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Jonathannn Doe"}'
```

**Update both name and age**
```bash
curl -X PATCH "http://localhost:8000/students/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Johnathan Doe", "age": 22}'
```

**Delete a student**
```bash
curl -X DELETE "http://localhost:8000/students/1"
```

### Validation Tests

**Invalid age (out of 17–25 range)**
```bash
curl -X POST "http://localhost:8000/students/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Bob", "age": 30}'
```

**Name with only spaces — rejected**
```bash
curl -X POST "http://localhost:8000/students/" \
  -H "Content-Type: application/json" \
  -d '{"name": "   ", "age": 20}'
```

**Name with surrounding spaces — auto-cleaned**
```bash
curl -X POST "http://localhost:8000/students/" \
  -H "Content-Type: application/json" \
  -d '{"name": "   Jane Doe   ", "age": 20}'
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
├── main.py        # FastAPI app, Pydantic models, and endpoints
└── students.db    # SQLite database (auto-created on first run)
```
