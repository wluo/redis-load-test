#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This is a port of the PING test from redis-benchmark.
This script will use locust as framework.

Author:- OpsTree Solutions
Author:- Will Luo
"""

from locust_redis_client import *


class RedisLocust(User):
    def __init__(self, *args, **kwargs):
        super(RedisLocust, self).__init__(*args, **kwargs)
        self.client = RedisClient()

    wait_time = constant(0)

    @task
    def get_ping_time(self):
        self.client.execute('ping', 'PING')

    @task
    def get_ping_message_time(self):
        self.client.execute('ping_with_message', 'PING', 'ping with a message')
 
    #@task
    def get_ping_message_pipelined(self):
        pipe = self.client.rc.pipeline()
        for i in range(6):
            pipe.pipeline_execute_command('PING', 'ping with message (pipelined)')

        self.client.execute_pipeline('pipelined pings (6x)', pipe)

