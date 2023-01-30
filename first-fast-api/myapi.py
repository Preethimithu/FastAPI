from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

# This is just import fastAPI,like an object to work
app = FastAPI()


# To creating like an instance of the fastAPI object
@app.get("/")  # only slash means homepage
def index():
    return {"name": "First Data"}

# sample data
students = {
    1: {
        "name": "Eman",
        "age": 26,
        "role": "SD"
    }
}

class Student(BaseModel):
    name: str
    age: int
    role: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    role: Optional[str] = None

# Path parameter
@app.get("/get-student/{student_id}")
# getting student_id as a parameter
def get_student(student_id: int = Path(None, description="The ID of the student you want to view", gt=0, lt=3)):
    # using path parameter. gt means greater-than, lt means lesser-than
    return students[student_id]
    # for returning the sample data

# Query parameter
# get method
@app.get("/get-by-name")
def get_student(name: str):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not Found"}


# post method
@app.post("/create-student/{student_id}")
def create_student(student_id : int, student : Student):
    if student_id in students:
        return {"Error": "Student Exists"}
    students[student_id] = student
    return students[student_id]

# put method
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.role != None:
        students[student_id].role = student.role
    return students[student_id]

# delete method
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    del students[student_id]
    return {"Message": "Student deleted successfully"}