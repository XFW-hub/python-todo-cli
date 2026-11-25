
from sqlalchemy import create_engine, text
from sqlalchemy.exc import TimeoutError


engine = create_engine(
    "postgresql+psycopg://"
    "test_user:test_password"
    "@127.0.0.1:5433/todo_test_db",

    pool_size=2,
    max_overflow=1,
    pool_timeout=3,
    pool_pre_ping=True,
    echo_pool="debug",
)

connections = []

try:
    for i in range(4):
        print(f"\n尝试获取第 {i + 1} 个连接")

        try:
            conn = engine.connect()
            connections.append(conn)

            pid = conn.execute(
                text("SELECT pg_backend_pid()")
            ).scalar_one()

            print("数据库进程 PID:", pid)
            print(engine.pool.status())

        except TimeoutError:
            print("连接池已满，获取连接超时")

finally:
    for conn in connections:
        conn.close()

    print("\n归还所有连接：")
    print(engine.pool.status())

    engine.dispose()
