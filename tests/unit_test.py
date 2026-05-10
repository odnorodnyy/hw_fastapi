import pytest
from crud import create_task, get_task, get_tasks, get_priority_tasks, search_tasks, update_task, delete_task
from schemas import TaskCreate, TaskUpdate, TaskSort

# Создаём задачу и проверяем что она появилась в БД
def test_create_task(db):
    task = TaskCreate(title="Тестовая задача", priority=3)
    res = create_task(db, task)
    assert res.id is not None                               # id должен проставиться автоматически
    assert res.title == "Тестовая задача"
    assert res.priority == 3
    assert res.status == "pending"
    assert res.created is not None                          # Дата должна проставиться автоматическ

# Проверяем дефолтные значения — только заголовок обязателен
def test_create_task_default(db):
    task = TaskCreate(title="Минимальная задача")
    res = create_task(db, task)
    assert res.description is None
    assert res.priority == 5
    assert res.status == "pending"

# Создаём задачу и получаем её по id
def test_get_task(db):
    task = TaskCreate(title="Тестируем")
    created = create_task(db, task)
    found = get_task(db, created.id)
    assert found is not None
    assert found.id == created.id
    assert found.title == "Тестируем"

# Несуществющая задача
def test_get_task_nf(db):
    res = get_task(db, 9999)
    assert res is None

# Пустая БД
def test_get_tasks_empty(db):
    result = get_tasks(db)
    assert result == []

# Создаём несколько задач и получаем все
def test_get_tasks(db):
    create_task(db, TaskCreate(title="Задача 1"))
    create_task(db, TaskCreate(title="Задача 2"))
    create_task(db, TaskCreate(title="Задача 3"))
    res = get_tasks(db)
    assert len(res) == 3


@pytest.mark.parametrize("sort_field", [
    TaskSort.title,
    TaskSort.status,
    TaskSort.priority,
    TaskSort.created
])

# Сортировка для каждого поля
def test_get_tasks_sorting(db, sort_field):
    create_task(db, TaskCreate(title="Б задача", priority=2))
    create_task(db, TaskCreate(title="В задача", priority=3))
    create_task(db, TaskCreate(title="А задача", priority=1))
    res = get_tasks(db, sort_by=sort_field)
    assert len(res) == 3

# Сортировка по приоритету
def test_get_tasks_sort_priority(db):
    create_task(db, TaskCreate(title="Низкий", priority=10))
    create_task(db, TaskCreate(title="Средний", priority=6))
    create_task(db, TaskCreate(title="Высокий", priority=1))
    res = get_tasks(db, sort_by=TaskSort.priority)
    assert res[0].priority == 1
    assert res[1].priority == 6
    assert res[2].priority == 10

# Поиск по заголовку
def test_search_tasks_title(db):
    create_task(db, TaskCreate(title="Подготовиться к кр по матану"))
    create_task(db, TaskCreate(title="Подготовиться к коллоку по линалу"))
    res = search_tasks(db, "кр")
    assert len(res) == 1
    assert res[0].title == "Подготовиться к кр по матану"

# Поиск по описанию
def test_search_tasks_description(db):
    create_task(db, TaskCreate(title="Подготовиться к кр по матану", description="Дата 14.05.2026"))
    create_task(db, TaskCreate(title="Подготовиться к коллоку по линалу", description="Отсутвует"))
    res = search_tasks(db, "Дата")
    assert len(res) == 1

# Создаём и обновляем задачу
def test_update_task(db):
    task = create_task(db, TaskCreate(title="Старый заголовок"))
    updated = update_task(db, task.id, TaskUpdate(title="Новый заголовок"))
    assert updated.title == "Новый заголовок"
    assert updated.id == task.id

# Меняем только статус, заголовок остаётся
def test_update_task_half(db):
    task = create_task(db, TaskCreate(title="Задача", priority=3))
    updated = update_task(db, task.id, TaskUpdate(status="done"))
    assert updated.status == "done"
    assert updated.title == "Задача"
    assert updated.priority == 3

# Создаём и удаляем задачу
def test_delete_task(db):
    task = create_task(db, TaskCreate(title="Удаленная задача"))
    deleted = delete_task(db, task.id)
    assert deleted.id == task.id
    assert get_task(db, task.id) is None

# Удаление несуществующей задачи
def test_delete_task_nf(db):
    res = delete_task(db, 9999)
    assert res is None