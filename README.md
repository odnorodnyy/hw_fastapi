# Task Manager API

Домашняя работа по созданию менеджера задач на `FastAPI` с веб приложением на Streamlit.

## Ссылки

- [API (Swagger)](https://hw-fastapi-32mp.onrender.com/docs)
- [Веб приложение](https://hwfastapi.streamlit.app/)

## Функции
- Создание, просмотр, обновление и удаление задач (CRUD)
- Сортировка задач по заголовку, статусу, приоритету и дате
- Поиск по тексту в заголовке и описании задачи
- Отдельное окно с выборокой топ N задач по приоритету
- Веб приложение на Streamlit

## Стек
```
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Streamlit
```
## P.S
Сервер на Render с бесплатным тарифом, поэтому он засыпает через минут 15-20 простоя.

Мини-инструкция по запуску и тесту:
1. Сначала открываем Swagger по ссылке выше
2. Ждем около минут, чтоб сервер очнулся
3. Если появилась страница Swagger с интерфейсом - успех
4. Теперь можно открывать Streamlit и тестировать

---

# Task Manager API part 2

Вторая часть домашней работы - тестирование написанного API.
Реализация трёх типов тестов:
- Юнит-тесты: проверка функций из `crud.py` напрямую через БД
- Функциональные тесты: проверка всех эндпоинтов через `TestClient`
- Нагрузочные тесты: проверка производительности через Locust

## Запуск по отдельности
```bash
# Юнит-тесты
pytest tests/unit_test.py -v

# Функциональные тесты
pytest tests/api_test.py -v
```

## Проверка покрытия
```bash
coverage run --source=main -m pytest tests/
coverage html
```
Покрытие кода тестами 94%. Отчёт о покрытии находится по пути `htmlcov/index.html`.


## Нагрузочное тестирование (Locust)

Запусти Locust (сервер уже запущен на Render):
```bash
locust -f tests/locust.py --host=https://hw-fastapi-32mp.onrender.com
```
Откройте `http://localhost:8089` в браузере

> Перед запуском убедиться, что сервер проснулся - откройте [Swagger](https://hw-fastapi-32mp.onrender.com/docs) и подождите загрузки.

Для запуска локально:
```bash
# Терминал 1
cd main
uvicorn main:app --reload

# Терминал 2
locust -f tests/locust.py --host=http://localhost:8000
```