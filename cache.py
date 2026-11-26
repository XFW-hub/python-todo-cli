
import json
import logging
import os

import redis
from redis.exceptions import RedisError


logger = logging.getLogger(__name__)


class TaskCache:

    TASKS_KEY = "todo:v1:tasks"

    def __init__(self, url=None, ttl=60):
        self.ttl = ttl
        self.client = None

        if url:
            self.client = redis.Redis.from_url(
                url,
                decode_responses=True,
                socket_connect_timeout=1,
                socket_timeout=1,
            )

    def get_tasks(self):
        if self.client is None:
            return None

        try:
            value = self.client.get(
                self.TASKS_KEY
            )

            if value is None:
                return None

            return json.loads(value)

        except (RedisError, ValueError):
            logger.warning(
                "Failed to read task cache",
                exc_info=True,
            )
            return None

    def set_tasks(self, tasks):
        if self.client is None:
            return

        try:
            self.client.set(
                self.TASKS_KEY,
                json.dumps(
                    tasks,
                    ensure_ascii=False,
                ),
                ex=self.ttl,
            )

        except RedisError:
            logger.warning(
                "Failed to write task cache",
                exc_info=True,
            )

    def invalidate(self):
        if self.client is None:
            return

        try:
            self.client.delete(
                self.TASKS_KEY
            )

        except RedisError:
            logger.warning(
                "Failed to invalidate task cache",
                exc_info=True,
            )

    def close(self):
        if self.client is not None:
            self.client.close()


def create_cache():
    return TaskCache(
        url=os.getenv("REDIS_URL"),
        ttl=int(
            os.getenv("CACHE_TTL", "60")
        ),
    )
