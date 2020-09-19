#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This is a script to Get and Set key in Redis Server for load testing.
This script will use locust as framework.

Author:- OpsTree Solutions
"""

from locust_redis_client import *

class RedisLocust(User):
    def __init__(self, *args, **kwargs):
        super(RedisLocust, self).__init__(*args, **kwargs)
        self.client = RedisClient()
        self.key = 'key1'
        self.value = 'value1'

#class RedisLua(RedisLocust):
#    min_wait = 100
#    max_wait = 100

    wait_time = between(0, 0.2)

    @task(2)
    def get_time(self):
        for i in range(100):
            self.key='key'+str(i)
            self.client.query(self.key)

    @task(1)
    def write(self):
        for i in range(100):
            self.key='key'+str(i)
            self.value='value'+str(i)
            self.client.write(self.key,self.value)

    @task(1)
    def get_key(self):
        var=str(randint(1,99))
        self.key='key'+var
        self.value='value'+var

