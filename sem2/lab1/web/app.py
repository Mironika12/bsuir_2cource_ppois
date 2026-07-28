from __future__ import annotations
from fastapi import FastAPI, HTTPException, Depends
from datetime import date
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from services.auth_service import AuthService
from services.storage_service import StorageService
from services.validate_service import ValidationService
from domain.student import Student
from domain.project_manager import ProjectManager
from domain.course_project import CourseProject
from domain.deadline import Deadline

app = FastAPI()
validator = ValidationService()
storage = StorageService()
auth = AuthService(storage, validator)

app.mount("/static", StaticFiles(directory="web/static"), name="static")


def get_project_data(student_id: str) -> dict:
    users = storage.load_users()

    user_data = users.get(student_id)
    if not user_data:
        raise HTTPException(status_code=404, detail=str("Пользователь не найден."))

    student = Student(user_data["student_name"], student_id)
    project_manager = ProjectManager(user_data["project_manager_name"])

    project = storage.load_project(
        user_data["project_file"],
        student,
        project_manager,
    )
    
    project_data = storage.project_to_dict(project)
    return project_data
        

def get_user_data(student_id: str) -> dict:
    users = storage.load_users()
    user_data = users.get(student_id)
    if not user_data:
        raise HTTPException(status_code=404, detail=str("Пользователь не найден."))
    
    return user_data
    

def load_project(project_data: dict) -> CourseProject:
    project = CourseProject()
    storage.dict_to_project(project_data, project)
    return project


def save_project(user_data: dict, project: CourseProject) -> dict:
    storage.save_project(user_data["project_file"], project)
    return storage.project_to_dict(project)

# ---------------------------------------

@app.get("/")
def home():
    return FileResponse("web/html/index.html")


@app.post("/login")
def login(student_id: str, pin: str):
    try:
        user_data = auth.login(student_id, pin)
        return user_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.post("/register")
def register(student_id: str, student_name: str, project_manager_name: str, pin: str):
    try:
        user_data = auth.register(student_id, student_name, project_manager_name, pin)
        return user_data

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

from fastapi import HTTPException

@app.get("/projects/{student_id}")
def get_project(student_id: str):
    try:
        return get_project_data(student_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/projects/{student_id}/theme")
def choose_theme(theme: str, user_data = Depends(get_user_data), project_data = Depends(get_project_data)):
    try:
        project = load_project(project_data)
        project.choose_theme(theme)
        return save_project(user_data, project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/projects/{student_id}/plan")
def add_item(item: dict, user_data = Depends(get_user_data), project_data = Depends(get_project_data)):
    print(item)
    item["deadline"] = Deadline(validator.parse_date(item["deadline"]))
    try:
        project = load_project(project_data)
        project.add_plan_item(item)
        return save_project(user_data, project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.delete("/projects/{student_id}/plan/{item_num}")
def remove_item(item_num: int, user_data = Depends(get_user_data), project_data = Depends(get_project_data)):
    try:
        project = load_project(project_data)
        project.remove_plan_item(item_num)
        return save_project(user_data, project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/projects/{student_id}/references")
def add_reference(ref: dict, user_data = Depends(get_user_data), project_data = Depends(get_project_data)):
    try:
        project = load_project(project_data)
        project.add_reference(ref)
        return save_project(user_data, project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/projects/{student_id}/references/read")
def mark_as_read(num: int, user_data = Depends(get_user_data), project_data = Depends(get_project_data)):
    try:
        project = load_project(project_data)
        project.research.mark_as_read(num)
        return save_project(user_data, project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/projects/{student_id}/write")
def write(text: str, user_data = Depends(get_user_data), project_data = Depends(get_project_data)):
    try:
        project = load_project(project_data)
        project.write_section(text)
        return save_project(user_data, project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.patch("/projects/{student_id}/deadline")
def set_deadline(deadline_date: str, user_data = Depends(get_user_data), project_data = Depends(get_project_data)):
    deadline = Deadline(validator.parse_date(deadline_date))
    try:
        project = load_project(project_data)
        project.set_deadline(deadline)
        return save_project(user_data, project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/projects/{student_id}/consultation")
def set_consultation(consultation_date: str, user_data = Depends(get_user_data), project_data = Depends(get_project_data)):
    try:
        project = load_project(project_data)
        project.add_consultation(validator.parse_date(consultation_date))
        return save_project(user_data, project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/projects/{student_id}/submit")
def submit(user_data = Depends(get_user_data), project_data = Depends(get_project_data)):
    try:
        project = load_project(project_data)
        project.submit()
        return save_project(user_data, project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))