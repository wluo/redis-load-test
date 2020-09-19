#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This is a port of the PING test from redis-benchmark.
This script will use locust as framework.

Author:- OpsTree Solutions
Author:- Will Luo
"""

from locust_redis_client import *


class RedisLocustGetTest(User):
    def __init__(self, *args, **kwargs):
        super(RedisLocustGetTest, self).__init__(*args, **kwargs)
        self.client = LocustRedisClient()

    wait_time = constant(0.01)

    @task
    def get_random_value(self):
        key = f'key:{{{tag}}}:{ randint(1, 100000000) }'
        self.client.query(key, name='get_test')

