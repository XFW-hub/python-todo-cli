
from todo import TodoList


def main():
    todo = TodoList()

    # 启动时读取历史任务
    try:
        todo.load_tasks()
    except (OSError, ValueError) as e:
        print(f"加载任务失败：{e}")
        return

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
                todo.save_tasks()
                print("任务添加并保存成功！")
            except ValueError as e:
                print(e)
            except OSError as e:
                print(f"任务已添加到内存，但保存失败：{e}")

        elif choice == "2":
            tasks = todo.get_tasks()

            if not tasks:
                print("当前没有任务。")
            else:
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")

        elif choice == "3":
            try:
                number = int(
                    input("请输入任务编号: ")
                )

                removed = todo.delete_task(number)
                todo.save_tasks()

                print(f"已删除并保存任务: {removed}")

            except ValueError:
                print("请输入整数编号")
            except IndexError as e:
                print(e)
            except OSError as e:
                print(f"任务已从内存删除，但保存失败：{e}")

        elif choice == "4":
            print("再见！")
            break

        else:
            print("无效选项，请重新输入。")


if __name__ == "__main__":
    main()
