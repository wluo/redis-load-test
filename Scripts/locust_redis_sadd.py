#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This is a port of the SADD test from redis-benchmark.
This script will use locust as framework.

Author:- OpsTree Solutions
Author:- Will Luo
"""

from locust_redis_client import *


class RedisLocustSaddTest(User):
    def __init__(self, *args, **kwargs):
        super(RedisLocustSaddTest, self).__init__(*args, **kwargs)
        self.client = LocustRedisClient()

    wait_time = constant(0.01)

    @task
    def sadd_test(self):
        key = f'myset:{{{ tag }}}'
        val = randint(0, 1000000000)
        self.client.execute('sadd_test', 'SADD', key, val)

