#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This is a port of the PING test from redis-benchmark.
This script will use locust as framework.

Author:- OpsTree Solutions
Author:- Will Luo
"""

from locust_redis_client import *


class RedisLocustRpopTest(User):
    def __init__(self, *args, **kwargs):
        super(RedisLocustRpopTest, self).__init__(*args, **kwargs)
        self.client = LocustRedisClient()

    wait_time = constant(0.01)

    @task
    def rpop_test(self):
        key = f'mylist:{{{ tag }}}'
        self.client.execute('rpop_test', 'RPOP', key)

