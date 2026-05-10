# Функциональные тесты это как Swagger, но автоматически

import pytest
from schemas import TaskSort

def test_create_task(client):
    res = client.post("/tasks", json={"title": "Тестовая задача", "priority": 3})
    assert res.status_code == 201
    data = res.json()
    assert data["id"] is not None
    assert data["title"] == "Тестовая задача"
    assert data["priority"] == 3
    assert data["status"] == "pending"
    assert data["created"] is not None

def test_create_task_default(client):
    res = client.post("/tasks", json={"title": "Минимальная задача"})
    assert res.status_code == 201
    data = res.json()
    assert data["description"] is None
    assert data["priority"] == 5
    assert data["status"] == "pending"

def test_get_task(client):
    created = client.post("/tasks", json={"title": "Тестируем"}).json()
    res = client.get(f"/tasks/{created['id']}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == created["id"]
    assert data["title"] == "Тестируем"

def test_get_task_nf(client):
    res = client.get("/tasks/9999")
    assert res.status_code == 404

def test_get_tasks_empty(client):
    res = client.get("/tasks")
    assert res.status_code == 200
    assert res.json() == []

def test_get_tasks(client):
    client.post("/tasks", json={"title": "Задача 1"})
    client.post("/tasks", json={"title": "Задача 2"})
    client.post("/tasks", json={"title": "Задача 3"})
    res = client.get("/tasks")
    assert res.status_code == 200
    assert len(res.json()) == 3


@pytest.mark.parametrize("sort_field", [
    TaskSort.title,
    TaskSort.status,
    TaskSort.priority,
    TaskSort.created
])
def test_get_tasks_sorting(client, sort_field):
    client.post("/tasks", json={"title": "Б задача", "priority": 2})
    client.post("/tasks", json={"title": "В задача", "priority": 3})
    client.post("/tasks", json={"title": "А задача", "priority": 1})
    sort_value = sort_field.value
    res = client.get(f"/tasks?sort_by={sort_value}")
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_get_tasks_sort_priority(client):
    client.post("/tasks", json={"title": "Низкий", "priority": 10})
    client.post("/tasks", json={"title": "Средний", "priority": 6})
    client.post("/tasks", json={"title": "Высокий", "priority": 1})
    res = client.get("/tasks?sort_by=priority")
    assert res.status_code == 200
    tasks = res.json()
    assert tasks[0]["priority"] == 1
    assert tasks[1]["priority"] == 6
    assert tasks[2]["priority"] == 10


def test_search_tasks_title(client):
    client.post("/tasks", json={"title": "Подготовиться к кр по матану"})
    client.post("/tasks", json={"title": "Подготовиться к коллоку по линалу"})
    res = client.get("/tasks/search?text=кр")
    assert res.status_code == 200
    tasks = res.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Подготовиться к кр по матану"

def test_search_tasks_description(client):
    client.post("/tasks", json={"title": "Подготовиться к кр по матану", "description": "Дата 14.05.2026"})
    client.post("/tasks", json={"title": "Подготовиться к коллоку по линалу", "description": "Отсутствует"})
    res = client.get("/tasks/search?text=Дата")
    assert res.status_code == 200
    assert len(res.json()) == 1

def test_update_task(client):
    created = client.post("/tasks", json={"title": "Старый заголовок"}).json()
    res = client.put(f"/tasks/{created['id']}", json={"title": "Новый заголовок"})
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Новый заголовок"
    assert data["id"] == created["id"]

def test_update_task_half(client):
    created = client.post("/tasks", json={"title": "Задача", "priority": 3}).json()
    res = client.put(f"/tasks/{created['id']}", json={"status": "done"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "done"
    assert data["title"] == "Задача"
    assert data["priority"] == 3

def test_delete_task(client):
    created = client.post("/tasks", json={"title": "Удаленная задача"}).json()
    res = client.delete(f"/tasks/{created['id']}")
    assert res.status_code == 200
    deleted = res.json()
    assert deleted["id"] == created["id"]
    get_res = client.get(f"/tasks/{created['id']}")
    assert get_res.status_code == 404

def test_delete_task_nf(client):
    res = client.delete("/tasks/9999")
    assert res.status_code == 404