
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Optional

app = FastAPI(title = "Student CRUD with pydantic validation")

# --- Pydantic Models ---



#Purpose: Validates data for creating a new student
#Used in: POST /students/ endpoint
#name	str	Required, 1-100 chars, no spaces-only, auto-stripped
#age	int	Required, 17-25 only
class StudentCreate(BaseModel): 
    #"... means This field is mandatory. The user MUST supply a value."
    name: str = Field(..., min_length=1, max_length=100, description="Student's full name")
    age: int = Field(..., ge=17, le=25, description="Student's age (1-120)")
    
    #Field() with min_length=1 will accept a string of spaces like " " as valid.
    #The @field_validator below REJECTS spaces as empty.

#     These ALL pass validation with Field() only:
#student1 = Student(name="John")        #  Valid
#student2 = Student(name="J")           #  Valid (1 character)
#student3 = Student(name="   ")         #  Valid? YES! length is 3, so passes!
#student4 = Student(name=" ")           #  Valid? YES! length is 1, so passes!
#student5 = Student(name="\n\t  ")      #  Valid? YES! whitespace counts as characters!



    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip(): # ← This checks for ACTUAL content after removing spaces
            raise ValueError("Name cannot be empty or just whitespace")
        return v.strip() # ← Also cleans the data!
    """
    @field_validator("age")
    @classmethod
    def block_specific_ages(cls, v: int) -> int:
        if v == 13:
            raise ValueError("Age 13 is not allowed")
        return v
"""


#Purpose: Shapes the output when sending student data back to client
# Used in: POST, GET, PATCH endpoints (anytime a student is returned)
#id	int	Database-generated ID
#name	str	Cleaned name
#age	int	Age value
class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    
    class Config:
        from_attributes = True  # For ORM-like compatibility (formerly `orm_mode`)

#This is a response schema.
#It tells FastAPI:
#“When I send a student back to the user, it must ALWAYS look like this.”







#Below is is a PATCH model (partial update model).
#It means: “User may send ONLY the fields they want to change.”
#Because Create model (must send everything)



#Purpose: Validates data for partially updating an existing student
#name	Optional[str]	Can be skipped; if provided, 1-100 chars, no spaces-only
#age	Optional[int]	Can be skipped; if provided, 1-120
#Used in: PATCH /students/{id} endpoint


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Student's full name")
    age: Optional[int] = Field(None, ge=17, le=25, description="Student's age (1-120)")
    
    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Name cannot be empty or just whitespace")
        return v.strip() if v else v
    


#Purpose: Shapes simple text responses (no student data)
#Used in: DELETE /students/{id} endpoint (returns {"detail": "Student deleted"})
class MessageResponse(BaseModel):
    detail: str


#Summary of the used Pydantic models
#------------------------------------
#Model	           Direction	            Required Fields     	Used In
#StudentCreate	   Incoming (request)   	name, age           	POST
#StudentResponse   Outgoing (response)	    id, name, age	        POST, GET, PATCH
#StudentUpdate	   Incoming (request)	    None (all optional)	    PATCH
#MessageResponse   Outgoing (response)	    detail	                DELETE
#------------------------------------


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


# --- CRUD Endpoints with Pydantic Models ---

# Create
#This function handles POST requests (used for creating data)


#@app.post("/students/")----Listens for POST requests at this URL
#response_model=StudentResponse----Returns data shaped like StudentResponse
#status_code=201----HTTP status = "Created"
#student: StudentCreate----FastAPI creates this object from request body

@app.post("/students/", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age) VALUES (?, ?)", 
        (student.name, student.age)
    )
    conn.commit()
    
    return StudentResponse(
        id=cur.lastrowid,
        name=student.name,
        age=student.age
    ) #This creates a new StudentResponse object that follows the StudentResponse schema.




# Read
@app.get("/students/{student_id}", response_model=StudentResponse)
def read_student(student_id: int):
    conn = get_db()
    student = conn.execute(
        "SELECT * FROM students WHERE id=?", 
        (student_id,)
    ).fetchone()
    
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return StudentResponse(
        id=student["id"],
        name=student["name"],
        age=student["age"]
    )


# Update (Partial update - PATCH is more appropriate for partial updates)
@app.patch("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student_update: StudentUpdate):
    conn = get_db()
    
    # First, check if student exists
    existing = conn.execute(
        "SELECT * FROM students WHERE id=?", 
        (student_id,)
    ).fetchone()
    
    if existing is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Build dynamic update query based on provided fields
    update_fields = []
    update_values = []
    
    if student_update.name is not None:
        update_fields.append("name = ?")
        update_values.append(student_update.name)
    
    if student_update.age is not None:
        update_fields.append("age = ?")
        update_values.append(student_update.age)
    
    if not update_fields:
        # No fields to update, return existing student
        return StudentResponse(
            id=existing["id"],
            name=existing["name"],
            age=existing["age"]
        )
    
    # Execute update
    update_values.append(student_id)
    cur = conn.cursor()
    cur.execute(
        f"UPDATE students SET {', '.join(update_fields)} WHERE id = ?",
        update_values
    )
    conn.commit()
    
    # Fetch and return updated student
    updated = conn.execute(
        "SELECT * FROM students WHERE id=?", 
        (student_id,)
    ).fetchone()
    
    return StudentResponse(
        id=updated["id"],
        name=updated["name"],
        age=updated["age"]
    )


# Delete
@app.delete("/students/{student_id}", response_model=MessageResponse)
def delete_student(student_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return MessageResponse(detail="Student deleted")


# Optional: Get all students endpoint
@app.get("/students/", response_model=list[StudentResponse])
def list_students(limit: int = 100, skip: int = 0):
    conn = get_db()
    students = conn.execute(
        "SELECT * FROM students LIMIT ? OFFSET ?",
        (limit, skip)
    ).fetchall()
    
    return [
        StudentResponse(id=s["id"], name=s["name"], age=s["age"])
        for s in students
    ]


