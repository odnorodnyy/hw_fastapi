from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from database import Base, engine, get_db
from schemas import TaskCreate, TaskUpdate, TaskResponse, TaskSort
import crud


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)                   # Создаём таблицы при запуске
    print("Таблицы созданы, сервер запущен")
    yield                                                   # Здесь сервер работает
    print("Сервер остановлен")

app = FastAPI(
    lifespan=lifespan,
    title="Task Manager",
    description="Домашнее задание по FastAPI по созданию менеджера задач"
)

def get_task_or_e(task_id: int, db: Session):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Задача {task_id} не найдена")
    return task


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(
        task: TaskCreate,
        db: Session = Depends(get_db)):
    return crud.create_task(db, task)

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
        sort_by: TaskSort | None  = Query(None, description="Поле для сортировки"),
        db: Session = Depends(get_db)):
    return crud.get_tasks(db, sort_by)

@app.get("/tasks/search", response_model=list[TaskResponse])
def search_tasks(
        text: str = Query(...,
                       min_length=1,
                       description="Текст для поиск"),
        db: Session = Depends(get_db)):
    return crud.search_tasks(db, text)


@app.get("/tasks/top", response_model=list[TaskResponse])
def get_top_tasks(
        n: int = Query(5,
                       ge=1,
                       le=100,
                       description="Количество задач"),
        db: Session = Depends(get_db)):
    return crud.get_priority_tasks(db, n)

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
        task_id: int,
        db: Session = Depends(get_db)):
    return get_task_or_e(task_id, db)

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
        task_id: int,
        task_update: TaskUpdate,
        db: Session = Depends(get_db)):
    get_task_or_e(task_id, db)
    return crud.update_task(db, task_id, task_update)

@app.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_task(
        task_id: int,
        db: Session = Depends(get_db)):
    get_task_or_e(task_id, db)
    return crud.delete_task(db, task_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)