
from todo import TodoList


def main():
    todo = TodoList()

    while True:
        print("\n===== Todo List =====")
        print("1. 添加任务")
        print("2. 查看任务")
        print("3. 删除任务")
        print("4. 退出程序")

        choice = input("请选择操作 (1/2/3/4): ")

        if choice == "1":
            task = input("请输入任务内容: ")
            try:
                todo.add_task(task)
                print("任务添加成功！")
            except ValueError as e:
                print(e)

        elif choice == "2":
            tasks = todo.get_tasks()
            if not tasks:
                print("当前没有任务。")
            else:
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")

        elif choice == "3":
            try:
                number = int(input("请输入任务编号: "))
                removed = todo.delete_task(number)
                print(f"已删除任务: {removed}")
            except ValueError:
                print("请输入整数编号")
            except IndexError as e:
                print(e)

        elif choice == "4":
            print("再见！")
            break

        else:
            print("无效选项，请重新输入。")


if __name__ == "__main__":
    main()
