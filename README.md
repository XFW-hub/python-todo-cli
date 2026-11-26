# Python Todo CLI

A simple command-line Todo List application built with Python.

## Features

- Add new tasks
- View all tasks
- Exit the application
- Simple and beginner-friendly command-line interface

## Requirements

- Python 3.8 or later
- No third-party dependencies

## Installation

Clone the repository:

```bash
git clone https://github.com/XFW-hub/python-todo-cli.git
```

Navigate to the project directory:

```bash
cd python-todo-cli
```

## Usage

Run the application:

```bash
python3 main.py
```

Example:

```text
===== Todo List =====
1. 添加任务
2. 查看任务
3. 退出程序

请选择操作 (1/2/3): 1
请输入任务内容: Learn Git
任务添加成功！
```

## Project Structure

```text
python-todo-cli/
├── main.py
├── README.md
├── .gitignore
└── LICENSE
```

## Roadmap

- [x] Add tasks
- [x] View tasks
- [x] Mark tasks as completed
- [x] Delete tasks
- [x] Save tasks to a JSON file

## License

This project is licensed under the MIT License. See the LICENSE file for details.


## Running Tests

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt

## Features

- Add new tasks
- View all tasks
- Delete tasks by number
- Automatically save tasks to a local JSON file
- Restore previous tasks when the application restarts
- Handle invalid task inputs and data files

## Data Persistence

Task data is stored locally in `tasks.json`.

The file is automatically created when tasks are saved and loaded when the application starts.

The task data file is excluded from Git version control.

## Testing

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run all tests:

```bash
python -m pytest -v
```

## Run with Docker

Build the Docker image:

```bash
docker build -t python-todo-cli:docker-demo .
```

Run the application:

```bash
docker run -it --rm python-todo-cli:docker-demo
```

To preserve tasks between container runs, create a Docker volume:

```bash
docker volume create todo-cli-data
```

Then start the application with the volume mounted:

```bash
docker run -it --rm \
  -v todo-cli-data:/app/data \
  python-todo-cli:docker-demo
```

Task data is saved in the Docker-managed volume and can be reused by future containers.

## Continuous Integration

GitHub Actions automatically:

- Runs the pytest test suite
- Builds the Docker image
- Reports the result on pull requests targeting `main`


## FastAPI Web Service

Python Todo CLI also provides a REST API built with FastAPI.

### Run locally

Install dependencies:

```bash
python -m pip install -r requirements-api.txt
```

Start the API server:

```bash
python -m uvicorn api:app --reload
```

API documentation:

http://127.0.0.1:8000/docs

### Available endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

### Run with Docker

Build the image:

```bash
docker build -f Dockerfile.web -t python-todo-api:dev .
```

Run the container:

```bash
docker run -d \
  --name todo-api \
  -p 127.0.0.1:8000:8000 \
  -v todo-api-data:/app/data \
  python-todo-api:dev
```

### Run tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

### Limitations

This API is intended for local development and learning. It has no authentication, uses a JSON file for storage, and is designed for a single server process.

## SQLite Database

The FastAPI service uses SQLite and SQLAlchemy ORM for persistent task storage.

### Features

- Stable auto-increment task IDs
- Create, read, update and delete tasks
- SQLAlchemy ORM models and transactions
- Persistent SQLite storage
- Automated database tests

### Run Locally

Install dependencies:

```bash
python -m pip install -r requirements-api.txt
```

Start the API:

```bash
python -m uvicorn api:app --reload
```

Open the API documentation:

http://127.0.0.1:8000/docs

### Run with Docker

Build:

```bash
docker build -f Dockerfile.web -t python-todo-api:sqlite-demo .
```

Create a volume:

```bash
docker volume create todo-sqlite-data
```

Run:

```bash
docker run -d \
  --name todo-sqlite-api \
  -p 127.0.0.1:8000:8000 \
  -v todo-sqlite-data:/app/data \
  python-todo-api:sqlite-demo
```

SQLite data is stored in `/app/data/tasks.db`.

### Run Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

### Notes

- The existing CLI still uses JSON storage.
- The FastAPI service uses SQLite.
- Existing JSON task data is not automatically imported.
- This API is intended for local development and learning, not public multi-user deployment.

## Database Migrations

This project uses Alembic to manage SQLite database schema changes.

### Initialize a New Database

```bash
alembic upgrade head
```

### Check Current Database Version

```bash
alembic current
```

### View Migration History

```bash
alembic history
```

### Check for Pending Schema Changes

```bash
alembic check
```

### Existing Databases

Databases created before Alembic was introduced require a one-time baseline registration.

After verifying the old schema and backing up the database:

```bash
alembic stamp baseline_tasks
alembic upgrade head
```

Do not stamp an empty database or a database with an unknown schema.

### New Task Fields

- `completed`: whether a task has been completed
- `created_at`: creation timestamp, stored in UTC

### Complete a Task

```bash
curl -X PATCH \
  http://127.0.0.1:8000/tasks/1/complete
```

### Important Notes

- Back up existing databases before applying schema migrations.
- Existing task data is preserved by the migration.
- Historical tasks receive a migration-time timestamp because their original creation times were not stored.
- Alembic migration files are committed to Git together with application code.


## PostgreSQL and Docker Compose

The FastAPI service supports PostgreSQL as an independent database service.

Docker Compose manages three services:

- `db`: PostgreSQL 17 database
- `migrate`: Alembic database migration job
- `api`: FastAPI application

### Requirements

- Docker Desktop
- Docker Compose v2

### Configuration

Create a local environment file:

```bash
cp .env.example .env
```

Set a strong `POSTGRES_PASSWORD` in `.env`.

Do not commit `.env` to Git.

### Start the Application

```bash
docker compose up -d --build
```

### View Service Status

```bash
docker compose ps -a
```

### Access the API

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

### Inspect PostgreSQL

```bash
docker compose exec db psql -U todo_user -d todo_db
```

### View Logs

```bash
docker compose logs api
docker compose logs db
docker compose logs migrate
```

### Stop the Application

```bash
docker compose down
```

The PostgreSQL named volume is retained by default.

**Warning:** `docker compose down -v` deletes Compose-managed named volumes and can destroy database data.

### Database Compatibility

- The CLI retains JSON storage.
- SQLite remains supported for local development and tests.
- Docker Compose uses PostgreSQL.
- SQLite data is not automatically transferred into PostgreSQL.
- Alembic manages schema initialization and future migrations.


## Database Engineering

### PostgreSQL Integration Tests

Start the isolated PostgreSQL test database:

```bash
docker compose -f compose.test.yaml up -d --wait
```

Run PostgreSQL integration tests:

```bash
RUN_POSTGRES_TESTS=1 python -m pytest -v -m postgres
```

Run all tests:

```bash
RUN_POSTGRES_TESTS=1 python -m pytest -v
```

Stop the test database:

```bash
docker compose -f compose.test.yaml down
```

### Connection Pool Configuration

The PostgreSQL connection pool supports the following environment variables:

| Variable | Default |
|---|---|
| DB_POOL_SIZE | 5 |
| DB_MAX_OVERFLOW | 10 |
| DB_POOL_TIMEOUT | 30 |
| DB_POOL_RECYCLE | 1800 |

Connection health checks are enabled using SQLAlchemy pool_pre_ping.

### Database Backup

Start the main application and execute:

```bash
./scripts/backup.sh
```

Backup files are stored in the local backups directory.

### Database Restore

Create a separate database:

```bash
docker compose exec db \
  createdb -U todo_user todo_restore_db
```

Restore a backup:

```bash
docker compose exec -T db \
  pg_restore -U todo_user \
  -d todo_restore_db \
  --exit-on-error \
  --single-transaction \
  < backups/todo.dump
```

Replace the backup filename with the actual backup file.

### Safety Notes

- Test databases are isolated from application data.
- Database backups must not be committed to Git.
- Restore backups into a separate database for verification.
- Docker volumes provide persistence but do not replace backups.

## Redis Caching

The application uses Redis to cache task list queries and reduce repeated PostgreSQL reads.

### Cache Strategy

- Cache Aside pattern
- Default cache TTL: 60 seconds
- Cache invalidation after successful database writes
- Database fallback when Redis is unavailable
- Approximate LRU eviction policy

PostgreSQL remains the source of truth. Redis is an optional caching layer.

### Configuration

| Environment Variable | Default |
|---|---|
| REDIS_URL | Disabled when not configured |
| CACHE_TTL | 60 |

Docker Compose configures Redis automatically.

### Start the Application

```bash
docker compose up -d --build
```

### Inspect Redis

```bash
docker compose exec redis redis-cli
```

```redis
GET todo:v1:tasks
TTL todo:v1:tasks
INFO stats
```

### Run Integration Tests

```bash
docker compose -f compose.test.yaml up -d --wait

RUN_POSTGRES_TESTS=1 RUN_REDIS_TESTS=1 \
python -m pytest -v
```

### Cache Failure Recovery

The application falls back to the database when Redis is unavailable.

```bash
docker compose stop redis
curl http://127.0.0.1:8000/tasks
docker compose start redis
```

### Limitations

The cache provides best-effort consistency through invalidation and TTL. Strong consistency, distributed cache rebuilding locks, and production Redis high availability are not implemented.

Redis is used only for rebuildable cache data and does not replace PostgreSQL persistence or backups.