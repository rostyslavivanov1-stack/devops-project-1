# DevOps Project 1: CPU Metrics Collector

Мультиконтейнерний клієнт-серверний додаток для збору, збереження та перегляду показників завантаження процесора.

## Склад системи

| Компонент | Опис |
|---|---|
| `host_monitoring_agent.py` | Агент на хості (без контейнера): щосекунди вимірює CPU і надсилає на сервер |
| `main.py` | REST API на FastAPI (у контейнері), зберігає метрики в SQLite |
| `sqlite-web` | Веб-інтерфейс для перегляду бази даних (у контейнері) |

Дані зберігаються в іменованому Docker volume `sqlite_data`, тому доступні після видалення та повторного створення контейнерів.

## Вимоги

- Docker Desktop (або Docker Engine + Docker Compose)
- Bash (Git Bash на Windows, WSL, Linux, macOS)
- Python 3.10+ (лише для запуску агента на хості)

## Запуск

### Варіант 1: Docker Compose (API + веб-інтерфейс БД)

```bash
bash run-compose.sh
```

Після запуску:

- API: http://localhost:8000 (документація: http://localhost:8000/docs)
- SQLite Web: http://localhost:8080

Зупинка (volume з даними зберігається):

```bash
bash stop-compose.sh
```

### Варіант 2: один контейнер (лише API)

```bash
bash run-manual.sh
bash stop-manual.sh
```

> Обидва варіанти використовують однаковий порт 8000, тому запускайте лише один із них одночасно.

### Моніторинговий агент (на хості)

```bash
pip install -r requirements-dev.txt
python host_monitoring_agent.py
```

Агент надсилає показники CPU на `http://localhost:8000/metrics`. Зупинка: `Ctrl+C`.

## API

| Метод | Шлях | Опис |
|---|---|---|
| GET | `/` | Перевірка стану |
| GET | `/metrics` | Останні 40 записів |
| POST | `/metrics` | Додати запис (`{"cpu_usage": 12.5}`) |
| DELETE | `/metrics/{metric_id}` | Видалити запис |

## Перевірка збереження даних

1. Запустіть систему й надішліть кілька метрик агентом.
2. Виконайте `bash stop-compose.sh`, потім `bash run-compose.sh`.
3. Відкрийте http://localhost:8000/metrics: старі записи на місці.

Інформація про volume: `docker volume inspect sqlite_data`
Інформація про мережу: `docker network inspect devops_project_1_app-network`

## Структура проєкту

```
.
├── main.py                    # FastAPI-сервер
├── host_monitoring_agent.py   # Агент на хості
├── Dockerfile
├── docker-compose.yml
├── requirements.txt           # Залежності сервера (контейнер)
├── requirements-dev.txt       # Залежності для локальної розробки та агента
├── run-manual.sh / stop-manual.sh
├── run-compose.sh / stop-compose.sh
├── .dockerignore
├── .gitignore
└── .gitattributes
```
