
import json
from pathlib import Path


class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        if not task.strip():
            raise ValueError("任务内容不能为空")
        self.tasks.append(task.strip())

    def get_tasks(self):
        return self.tasks.copy()

    def delete_task(self, task_number):
        if not 1 <= task_number <= len(self.tasks):
            raise IndexError("任务编号不存在")
        return self.tasks.pop(task_number - 1)

    def save_tasks(self, file_path="tasks.json"):
        path = Path(file_path)

        data = {"tasks": self.tasks}

        with path.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2
            )

    def load_tasks(self, file_path="tasks.json"):
        path = Path(file_path)

        if not path.exists():
            self.tasks = []
            return

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if (
            not isinstance(data, dict)
            or not isinstance(data.get("tasks"), list)
            or not all(
                isinstance(task, str)
                for task in data["tasks"]
            )
        ):
            raise ValueError("任务文件格式不正确")

        self.tasks = data["tasks"]
