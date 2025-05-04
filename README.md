## Task Service FastAPI Проект 🚀

### Стек технологий

* ![Python](https://img.shields.io/badge/Python-3.12-grey?style=plastic&logo=python&logoColor=white&labelColor=3776AB)
* ![FastAPI](https://img.shields.io/badge/FastAPI-0.111-grey?style=plastic&logo=fastapi&logoColor=white&labelColor=009688)
* ![Docker](https://img.shields.io/badge/Docker-v25.0.3-grey?style=plastic&logo=docker&logoColor=white&labelColor=2496ED)
* ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-grey?style=plastic&logo=postgresql&logoColor=white&labelColor=336791)
* ![Pytest](https://img.shields.io/badge/Pytest-8-grey?style=plastic&logo=pytest&logoColor=white&labelColor=0A9EDC)

---

### Описание проекта

**Task Service** — лёгкий REST‑сервис на FastAPI для управления личными задачами.  
Позволяет регистрироваться, авторизоваться по JWT, создавать, обновлять и искать задачи с фильтрами.

---

### Функционал

#### Модели

* **User** — имя, email, пароль (bcrypt‑хеш)  
* **Task** — заголовок, описание, статус (`pending` / `done`), приоритет, дата создания, владелец

#### Аутентификация

* Хеширование паролей (`passlib[bcrypt]`)  
* Пара токенов **access + refresh** (JWT)  
* Обновление access‑токена по refresh

#### Задачи

* CRUD + расширенные фильтры  
* Поиск подстроки в названии/описании  
* Все защищённые эндпоинты требуют `Authorization: Bearer <token>`

---

### API Endpoints

| Метод    | URL                | Описание                                                     |
| -------- | ------------------ | ------------------------------------------------------------ |
| **POST** | `/register`        | Регистрация пользователя                                     |
| **POST** | `/login`           | Получение пары JWT                                           |
| **POST** | `/refresh`         | Обновление access‑токена                                     |
| **POST** | `/tasks`           | Создать задачу                                               |
| **PUT**  | `/tasks/{id}`      | Обновить задачу                                              |
| **GET**  | `/tasks`           | Список задач c фильтрами `status`, `priority`, `created_at` |
| **GET**  | `/tasks/search?q=` | Поиск задач по подстроке                                     |

Интерактивная документация:  
- Swagger UI: `http://localhost:8000/docs`  
- Redoc:      `http://localhost:8000/redoc`

---

### Установка и запуск 🛠️

<details>
<summary>⚡️ Быстрый старт в Docker</summary>

1. **Клонировать репозиторий**
   ```bash
   git clone https://github.com/yourname/TestWork05.git
   cd TestWork05
   ```

2. **Запустить контейнеры**

   ```bash
   docker compose up --build
   ```

3. Через пару секунд сервис будет доступен на `http://localhost:8000/`.
   База данных поднимется автоматически, таблицы создаются при старте приложения.

</details>

#### Запуск тестов

```bash
docker compose exec api pytest -q
```

---

### Переменные окружения (`.env`)

| Переменная               | Описание                                    | Пример по‑умолчанию                                       |
| ------------------------ | ------------------------------------------- | --------------------------------------------------------- |
| `DATABASE_URL`           | URL подключения к базе (Postgres + asyncpg) | `postgresql+asyncpg://fastapi:fastapi@db:5432/fastapi_db` |
| `JWT_SECRET`             | Секрет для подписи JWT                      | `super-strong-random-string`                              |
| `ACCESS_EXPIRES_MINUTES` | Время жизни access‑токена (в минутах)       | `30`                                                      |
| `REFRESH_EXPIRES_DAYS`   | Время жизни refresh‑токена (в днях)         | `7`                                                       |

---

### Docker Setup

* **api** — контейнер FastAPI + Uvicorn
* **db**  — PostgreSQL 16‑alpine, том `postgres_data` для персистентности

---

### Лицензия

Проект распространяется под лицензией MIT — см. файл [LICENSE](LICENSE).

---

<details>
<summary><b>Связаться со мной</b></summary>
<p align="left">
  <a href="mailto:pafos.light@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-%23EA4335.svg?style=plastic&logo=gmail&logoColor=white" alt="Gmail"/>
  </a>
  <a href="https://t.me/petr_lip">
    <img src="https://img.shields.io/badge/Telegram-0088CC?style=plastic&logo=telegram&logoColor=white" alt="Telegram"/>
  </a>
</p>
</details>
