import streamlit as st
from datetime import datetime
import requests

API_URL = "https://hw-fastapi-32mp.onrender.com"
st.title("Менеджер задач")
st.text("Дополнение к домашней работе по FastAPI.\n"
        "Создал простенькую страничку для \"клиента\" и более удобной демостранции функционала")

# Словарь для перевода статусов
status_translate = {
    "В ожидании": "pending",
    "В работе": "in_progress",
    "Сделано": "done",
    "pending": "В ожидании",
    "in_progress": "В работе",
    "done": "Сделано"
}

# Словарь для перевода типов сортировки
sort_translate = {
    "-": "-",
    "title": "Названию",
    "status": "Статусу",
    "priority": "Приоритету",
    "created": "Дате создания"
}

reverse = {v: k for k, v in sort_translate.items() if k != "-"}

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Все задачи",
    "Создать задачу",
    "Обновить или удалить",
    "Поиск",
    "Топ по приоритету"
])


# Все задачи
with tab1:
    st.subheader("Список задач")
    sort = st.selectbox("Сортировать по:",
                        options=["-", "Заголовку", "Статусу", "Приоритету", "Дате создания"])
    sort_by = reverse.get(sort,"-")
    if st.button("Загрузить задачи"):
        params = {}
        if sort_by != "-":
            params["sort_by"] = sort_by
        # GET /tasks?sort_by
        response = requests.get(f"{API_URL}/tasks", params=params)
        if response.status_code == 200:
            tasks = response.json()
            if not tasks:
                st.info("Задач пока нет")
            else:
                for task in tasks:
                    dt = datetime.fromisoformat(task["created"])
                    status_ru = status_translate.get(task["status"], task["status"])
                    with st.expander(f"#{task["id"]} - {task["title"]}"):
                        st.write(f"Описание: {task["description"] or ''}")
                        st.write(f"Статус: {task["status"]}")
                        st.write(f"Приоритет: {task["priority"]}")
                        st.write(f"Создана: {dt.strftime('%d.%m.%Y %H:%M')}")
        else:
            st.error(f"Ошибка: {response.status_code}")

# Создать задачу
with tab2:
    st.subheader("Новая задача")
    title = st.text_input("Заголовок")
    description = st.text_area("Описание")
    status = st.selectbox("Статус", ["В ожидании", "В работе", "Сделано"])
    priority = st.slider("Приоритет (где 1 - важнее всего)",
                         min_value=1, max_value=10, value=5)
    if st.button("Создать задачу"):
        if not title:
            st.warning("Заголовок обязателен, повторите попытку")
        else:
            status_en = status_translate[status]
            # POST /tasks
            response = requests.post(f"{API_URL}/tasks", json={
                "title": title,
                "description": description,
                "status": status_en,
                "priority": priority
            })
            if response.status_code == 201:
                st.success(f"Задача создана, её ID: {response.json()["id"]}")
            else:
                st.error(f"Ошибка: {response.status_code}: {response.text}")


# Обновить или удалчить
with tab3:
    st.subheader("Обновить задачу")
    update_id = st.number_input("ID задачи", min_value=1, step=1, key="update_id")
    # Поля для обновления
    new_title = st.text_input("Новый заголовок (можно оставить пустым)")
    new_description = st.text_area("Новое описание (можно оставить пустым)")
    new_status = st.selectbox("Новый статус", ["-", "В ожидании", "В работе", "Сделано"])
    new_priority = st.slider("Новый приоритет (где 0 - не менять)",
                             min_value=0, max_value=10, value=0)
    # Собираем только те поля, которые заполнены
    if st.button("Обновить"):
        update_data = {}
        if new_title:
            update_data["title"] = new_title
        if new_description:
            update_data["description"] = new_description
        if new_status != "-":
            update_data["status"] = status_translate[new_status]
        if new_priority > 0:
            update_data["priority"] = new_priority
        if not update_data:
            st.warning("Необходимо заполнить хотя бы одно поле")
        else:
            # PUT /tasks/{id}
            response = requests.put(f"{API_URL}/tasks/{update_id}", json=update_data)
            if response.status_code == 200:
                st.success(f"Задача #{update_id} успешно обновлена")
                st.json(response.json())
            else:
                st.error(f"Ошибка: {response.status_code}: {response.text}")

    st.divider()

    st.subheader("Удалить задачу")
    delete_id = st.number_input("ID задачи для удаления",
                                min_value=1, step=1, key="delete_id")
    if st.button("Удалить", type="primary"):
        # DELETE /tasks/{id}
        response = requests.delete(f"{API_URL}/tasks/{delete_id}")
        if response.status_code == 200:
            st.success(f"Задача #{delete_id} удалена")
        else:
            st.error(f"Ошибка: {response.status_code}: {response.text}")


# Поиск
with tab4:
    st.subheader("Поиск по тексту задачи")
    query = st.text_input("Введи текст для поиска")
    if st.button("Найти"):
        if not query:
            st.warning("Введи текст для поиска")
        else:
            # GET /tasks/search
            response = requests.get(f"{API_URL}/tasks/search", params={"q": query})
            if response.status_code == 200:
                tasks = response.json()
                if not tasks:
                    st.info(f"Ничего не найдено по запросу \"{query}\"")
                else:
                    st.success(f"Найдено задач: {len(tasks)}")
                    for task in tasks:
                        status = status_translate.get(task["status"], task["status"])
                        with st.expander(f"#{task["id"]} - {task["title"]}"):
                            st.write(f"Описание: {task["description"] or "-"}")
                            st.write(f"Статус: {status}")
                            st.write(f"Приоритет: {task["priority"]}")
            else:
                st.error(f"Ошибка: {response.status_code}")

# Топ по приоритету
with tab5:
    st.subheader("Топ задач по приоритету")
    n = st.number_input("Сколько задач показать?",
                        min_value=1, max_value=100, value=5)
    if st.button("Показать топ"):
        # GET /tasks/top
        response = requests.get(f"{API_URL}/tasks/top", params={"n": n})
        if response.status_code == 200:
            tasks = response.json()
            if not tasks:
                st.info("Задач пока нет")
            else:
                st.table([{
                    "ID": t["id"],
                    "Заголовок": t["title"],
                    "Статус": status_translate.get(t["status"], t["status"]),
                    "Приоритет": t["priority"]
                } for t in tasks])
        else:
            st.error(f"Ошибка: {response.status_code}")