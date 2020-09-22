#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This script uses the locust framework.

We will generate keys (~60 chars) and vals (~160 chars) and do around 80% SETs and 20% GETs.

The key and value sizes are based on average key size of course-progress-sec.

Author:- OpsTree Solutions
Author:- Will Luo
"""

from locust_redis_client import *
from locust_redis_set_get_base import RedisLocustSetGetTestBase


class RedisLocustSetGet8020Test(RedisLocustSetGetTestBase):

    wait_time = constant(0.1)

    def __init__(self, *args, **kwargs):
        super(RedisLocustSetGet8020Test, self).__init__(*args, **kwargs)


    @task
    def get_values_task(self):
        self.get_random_values()


    @task(4)
    def set_values_task(self):
        self.set_random_values()

