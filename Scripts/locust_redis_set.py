#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This is a port of the PING test from redis-benchmark.
This script will use locust as framework.

Author:- OpsTree Solutions
Author:- Will Luo
"""

from locust_redis_client import *


class RedisLocustSetTest(User):
    def __init__(self, *args, **kwargs):
        super(RedisLocustSetTest, self).__init__(*args, **kwargs)
        self.client = LocustRedisClient()

    wait_time = constant(0.01)

    @task
    def set_random_value(self):
        key = f'key:{{{tag}}}:{ randint(1, 100000000) }'
        val = f'val_{ key }'
        self.client.write(key, val, name='set_test')

