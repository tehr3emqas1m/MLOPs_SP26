import sqlite3
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
#Lets make a function for this endpoint
def hello():
    dic1 = {"message": "Helo! This is a student Database API"}
    return dic1


# --- Database setup ---
def get_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
with get_db() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)
    conn.commit()

# --- CRUD Endpoints ---




# Create
@app.post("/students/")
def create_student(name: str, age: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    return {"id": cur.lastrowid, "name": name, "age": age}

# Read
@app.get("/students/{student_id}")
def read_student(student_id: int):
    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return dict(student)

# Update
@app.put("/students/{student_id}")
def update_student(student_id: int, name: str, age: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE students SET name=?, age=? WHERE id=?", (name, age, student_id))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"id": student_id, "name": name, "age": age}

# Delete
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted"}

