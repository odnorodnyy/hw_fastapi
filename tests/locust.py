from locust import HttpUser, task, between

# HttpUser класс, который описывает одного виртуаьлного пользователя
class TaskUser(HttpUser):
    wait_time = between(1, 5)                                   # between(1, 5) - пользователь ждёт от 1 до 5 секунд между запросами
    # on_start выполняется один раз когда пользователь "заходит"
    def on_start(self):
        for i in range(5):
            self.client.post("/tasks", json={
                "title": f"Задача {i}",
                "description": f"Описание задачи {i}",
                "status": "pending",
                "priority": i + 1
            })

    # @task помечаем метод как задачу пользователя; @task(3) запрос выполняется в 3 раза чаще чем @task(1)

    # Самый частый запрос будет просто получить все задачи
    @task(3)
    def get_tasks(self):
        self.client.get("/tasks")

    # Получить задачи с сортировкой
    @task(3)
    def get_tasks_sorted(self):
        self.client.get("/tasks?sort_by=priority")

    # Поиск по тексту
    @task(2)
    def search_tasks(self):
        self.client.get("/tasks/search?text=Задача")

    # Топ задач по приоритету
    @task(2)
    def get_top_tasks(self):
        self.client.get("/tasks/top?n=3")

    # Создание новой задачи
    @task(1)
    def create_task(self):
        self.client.post("/tasks", json={
            "title": "Нагрузочная задача",
            "status": "pending",
            "priority": 5
        })

    # Обновляем первую задачу
    @task(1)
    def update_task(self):
        self.client.put("/tasks/1", json={"status": "in_progress"})

    # Получаем задачу по id
    @task(1)
    def get_task_by_id(self):
        self.client.get("/tasks/1")