#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This is a port of the HSET test from redis-benchmark.
This script will use locust as framework.

Author:- OpsTree Solutions
Author:- Will Luo
"""

from locust_redis_client import *


class RedisLocustHsetTest(User):
    def __init__(self, *args, **kwargs):
        super(RedisLocustHsetTest, self).__init__(*args, **kwargs)
        self.client = LocustRedisClient()

    wait_time = constant(0.01)

    @task
    def hset_test(self):
        myhash = f'myhash:{{{ tag }}}'
        key = f'element:{ randint(0, 1000000) }'
        val = randint(0, 1000000000)
        self.client.execute('hset_test', 'HSET', myhash, key, val)

