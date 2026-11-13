
def main():
    tasks = []

    while True:
        print("\n===== Todo List =====")
        print("1. 添加任务")
        print("2. 查看任务")
        print("3. 删除任务")
        print("4. 退出程序")

        choice = input("请选择操作 (1/2/3/4): ")

        if choice == "1":
            task = input("请输入任务内容: ").strip()
            if task:
                tasks.append(task)
                print("任务添加成功！")
            else:
                print("任务内容不能为空。")

        elif choice == "2":
            if not tasks:
                print("当前没有任务。")
            else:
                for index, task in enumerate(tasks, start=1):
                    print(f"{index}. {task}")

        elif choice == "3":
            if not tasks:
                print("当前没有可删除的任务。")
                continue

            for index, task in enumerate(tasks, start=1):
                print(f"{index}. {task}")

            task_id = input("请输入要删除的任务编号: ").strip()

            if not task_id.isdigit():
                print("请输入有效的任务编号。")
                continue

            task_index = int(task_id) - 1

            if 0 <= task_index < len(tasks):
                removed_task = tasks.pop(task_index)
                print(f"已删除任务: {removed_task}")
            else:
                print("任务编号不存在。")

        elif choice == "4":
            print("再见！")
            break

        else:
            print("无效选项，请重新输入。")


if __name__ == "__main__":
    main()
  