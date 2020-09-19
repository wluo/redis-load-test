#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This is a port of the PING test from redis-benchmark.
This script will use locust as framework.

Author:- OpsTree Solutions
Author:- Will Luo
"""

from locust_redis_client import *


class RedisLocustLpushTest(User):
    def __init__(self, *args, **kwargs):
        super(RedisLocustLpushTest, self).__init__(*args, **kwargs)
        self.client = LocustRedisClient()

    wait_time = constant(0.01)

    @task
    def lpush_test(self):
        key = f'mylist:{{{ tag }}}'
        val = f'{ randint(1, 100000000) }'
        self.client.execute('lpush_test', 'LPUSH', key, val)

