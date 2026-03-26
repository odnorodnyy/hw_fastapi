from pydantic import BaseModel
from datetime import datetime
import enum

# Допустимые статусы задачи
class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

# Допустимые поля для сортировки
class TaskSort(str, enum.Enum):
    title= "title"
    status = "status"
    created = "created"
    priority = "priority"

# Что клиент присылает при создании задачи
class TaskCreate(BaseModel):
    title: str                                  # Обязательное поле
    description: str | None = None              # Необязательное, по умолчанию пусто
    status: TaskStatus = TaskStatus.pending     # По умолчанию "pending"
    priority: int = 5                           # По умолчанию средний приоритет (1-10)

# Что клиент присылает при обновлении задачи
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: int | None = None

# Что сервер возвращает клиенту
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: int
    created: datetime

    model_config = {"from_attributes": True}    # чтобы читать SQLAlchemy-объекты