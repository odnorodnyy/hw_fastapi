from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskSort

def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.model_dump())                         # task.model_dump() превращает в обычный словарь
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()    # filter - аналог WHERE в SQL, first() берём первый результат

def get_tasks(db: Session, sort_by: TaskSort = None):
    query = db.query(Task)                                      # SELECT * FROM tasks
    if sort_by == TaskSort.title:
        query = query.order_by(Task.title)                      # Сортировка по алфавиту
    elif sort_by == TaskSort.status:
        query = query.order_by(Task.status)                     # Сортировка по статусу
    elif sort_by == TaskSort.created:
        query = query.order_by(Task.created)                    # Сортировка по дате
    elif sort_by == TaskSort.priority:
        query = query.order_by(Task.priority)                   # Сортировка по приориттеу
    return query.all()

# Берём n задач с наименьшим числом приоритет
def get_priority_tasks(db: Session, n: int):
    return (
        db.query(Task)
        .order_by(Task.priority)                                # Сначала priority=1
        .limit(n)                                               # Берём только первые n штук
        .all()
    )

def search_tasks(db: Session, query_text: str):
    return (
        db.query(Task)
        .filter(
            Task.title.ilike(f"%{query_text}%") |
            Task.description.ilike(f"%{query_text}%"))
        .all()
    )

def update_task(db: Session, task_id: int, task_update: TaskUpdate):
    db_task = get_task(db, task_id)                             # Находим задачу
    if db_task is None:
        return None                                             # задача не найдена (вернём None)
    update_data = task_update.model_dump(exclude_unset=True)    # exclude_unset=True берём только те поля, которые клиент реально прислал
    for field, value in update_data.items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task is None:
        return None
    db.delete(db_task)                                          # Помечаем на удаление
    db.commit()                                                 # Применяем удаление
    return db_task                                              # возвращаем удалённый объект