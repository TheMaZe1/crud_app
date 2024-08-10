"""CRUD app for todo list"""
from fastapi import FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from database import Base, engine
import models
import schemas


Base.metadata.create_all(engine)

app = FastAPI()


@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoCreate):
    """Create todo item:
        - **task**: string with task
    """

    session = Session(bind=engine, expire_on_commit=False)

    todo = models.Todo(task=todo.task)

    session.add(todo)
    session.commit()

    id = todo.id

    session.close()
    return f"create todo with id: {id}"


@app.get("/todo/{id}", response_model=schemas.ToDo)
def read_todo(id: int):
    """Get task for id
        - **id**: id todo item
    """

    session = Session(bind=engine, expire_on_commit=False)

    todo = session.query(models.Todo).get(id)

    session.close()

    if not todo:
        raise HTTPException(status_code=404, detail=f"todo with id {id} not found")

    return todo

@app.put("/todo/{id}")
def update_todo(id: int, task: str):
    """Update task
        - **id**: id todo item
        - **task**: new string task
    """
    session = Session(bind=engine, expire_on_commit=False)

    todo = session.query(models.Todo).get(id)

    if todo:
        todo.task = task
        session.commit()
        return "update todo with {id}"
    
    session.close()

    if not todo:
        raise HTTPException(status_code=404, detail=f"todo with id: {id} not found")

@app.delete("/todo/{id}")
def delete_todo(id: int):
    """Delete todo item
        - **id**: id todo item
    """
    session = Session(bind=engine, expire_on_commit=False)

    todo = session.query(models.Todo).get(id)

    if todo:
        session.delete(todo)
        session.commit()
        return "delete todo with {id}"
    session.close()

    if not todo:
        raise HTTPException(status_code=404, detail=f"todo with id: {id} not found")

@app.get("/todo", response_model=list[schemas.ToDo])
def read_all_todo():
    """Return list of tasks"""

    session = Session(bind=engine, expire_on_commit=False)
    todos = session.query(models.Todo).all()
    session.close()

    return todos
