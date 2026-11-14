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