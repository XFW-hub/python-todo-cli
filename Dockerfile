
FROM python:3.12-slim

# 创建应用目录和数据目录
RUN mkdir -p /app/data

# 设置默认工作目录
WORKDIR /app/data

# 复制应用源代码
COPY main.py todo.py /app/

# 启动命令行程序
CMD ["python", "/app/main.py"]
