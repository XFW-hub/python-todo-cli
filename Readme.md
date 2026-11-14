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