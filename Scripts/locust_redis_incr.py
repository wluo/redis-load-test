#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This is a port of the PING test from redis-benchmark.
This script will use locust as framework.

Author:- OpsTree Solutions
Author:- Will Luo
"""

from locust_redis_client import *


class RedisLocustIncrTest(User):
    def __init__(self, *args, **kwargs):
        super(RedisLocustIncrTest, self).__init__(*args, **kwargs)
        self.client = LocustRedisClient()

    wait_time = constant(0.01)

    @task
    def incr_random_key(self):
        key = f'counter:{tag}:{ randint(1, 100000000) }'
        self.client.execute('incr_test', 'INCR', key)

