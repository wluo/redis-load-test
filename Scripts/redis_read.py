#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This is a script to Get key in Redis Server for load testing.
This script will use locust as framework.

Author:- OpsTree Solutions
"""

import json
import time
from locust import Locust, events, User, between
from locust import TaskSet, task
import redis
import gevent.monkey
gevent.monkey.patch_all()

def load_config(filepath):
    """For loading the connection details of Redis"""
    with open(filepath) as property_file:
        configs = json.load(property_file)
    return configs

filename = "redis.json"

configs = load_config(filename)

print(configs)

class RedisClient(object):
    def __init__(self, host=configs["redis_host"], port=configs["redis_port"], pw=configs['redis_password'], cert=configs['redis_cert']):
        self.rc = redis.StrictRedis(host=host, port=port, password=pw, ssl=True, ssl_certfile=cert, ssl_cert_reqs=None, ssl_check_hostname=False)
        print(host, port)

    def query(self, key, command='GET'):
        """Function to put GET request on Redis"""
        result = None
        start_time = time.time()
        result = self.rc.get(key)
        total_time = int((time.time() - start_time) *1000000)
        if not result:
            result = ''
            events.request_failure.fire(request_type=command, name=key, response_time=total_time, response_length=0, exception="Error")
        else:
            length = len(result)
            events.request_success.fire(request_type=command, name=key, response_time=total_time, response_length=length)
        return result

class RedisLocust(User):
    def __init__(self, *args, **kwargs):
        super(RedisLocust, self).__init__(*args, **kwargs)
        self.client = RedisClient()
        self.client.rc.set('key1', 'value1')
        self.client.rc.set('key2', 'value2')

    wait_time = between(0, 0.3)

    @task(1)
    def get_time(self):
        self.client.query('key1')



class RedisLua(RedisLocust):
    min_wait = 100
    max_wait = 100

    @task(1)
    def get_time(self):
        self.client.query('key2')

    wait_time = between(0, 0.5)

