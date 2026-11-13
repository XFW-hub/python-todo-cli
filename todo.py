
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
        return self.tasks.pop(task_number-1)
