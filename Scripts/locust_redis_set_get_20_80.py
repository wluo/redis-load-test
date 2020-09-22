#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This script uses the locust framework.

We will generate keys (~60 chars) and vals (~160 chars) and do around 20% SETs and 80% GETs.

The key and value sizes are based on average key size of course-progress-sec.

Author:- OpsTree Solutions
Author:- Will Luo
"""

from locust_redis_client import *
import random
import string


class RedisLocustSetGet2080Test(User):

    wait_time = constant(0.1)

    sample_size = 100

    def __init__(self, *args, **kwargs):
        super(RedisLocustSetGet2080Test, self).__init__(*args, **kwargs)
        self.client = LocustRedisClient()

        # generate 100 keys and values
        self.rand_keys = list()
        self.rand_vals = list()

        for i in range(RedisLocustSetGet2080Test.sample_size):
            self.rand_keys.append(RedisLocustSetGet2080Test.generate_key())
            self.rand_vals.append(RedisLocustSetGet2080Test.generate_value())
            self.client.write(self.rand_keys[i], self.rand_vals[i], name='seeding')


    @staticmethod
    def generate_key():
        user_id = str(randint(1, 999999999999)).rjust(12, '0')
        course_id = str(randint(1, 999999999)).rjust(9, '0')
        return 'course_last_viewed:user:{}:course:{}:filler'.format(user_id, course_id)


    @staticmethod
    def generate_value():
        item_id = str(randint(1, 999999999999)).rjust(12, '0')
        filler = ''.join(random.choice(string.ascii_letters) for i in range(72))
        return '{{"item_id": {}, "item_type": "lecture", "timestamp": {}, "filler": "{}"}}'.format(item_id, time.time(), filler)


    @task(4)
    def get_random_value(self):
        for i in range(5):
            self.client.query(random.choice(self.rand_keys), name='GET_5_keys')

    @task
    def set_random_value(self):
        for i in range(5):
            self.client.write(random.choice(self.rand_keys), random.choice(self.rand_vals), name='SET_5_keys')

