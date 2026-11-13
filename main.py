
def main():
    tasks = []

    while True:
        print("\n===== Todo List =====")
        print("1. 添加任务")
        print("2. 查看任务")
        print("3. 退出程序")

        choice = input("请选择操作 (1/2/3): ")

        if choice == "1":
            task = input("请输入任务内容: ")
            tasks.append(task)
            print("任务添加成功！")

        elif choice == "2":
            if not tasks:
                print("当前没有任务。")
            else:
                for index, task in enumerate(tasks, start=1):
                    print(f"{index}. {task}")

        elif choice == "3":
            print("再见！")
            break

        else:
            print("无效选项，请重新输入。")


if __name__ == "__main__":
    main()
  