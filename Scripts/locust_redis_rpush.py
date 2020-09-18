#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This is a port of the PING test from redis-benchmark.
This script will use locust as framework.

Author:- OpsTree Solutions
Author:- Will LUo
"""

import json
import time
from locust import Locust, User
from locust import between, constant, events, task
import redis
import gevent.monkey
gevent.monkey.patch_all()
from random import randint

def load_config(filepath):
    """For loading the connection details of Redis"""
    with open(filepath) as property_file:
        configs = json.load(property_file)
    return configs

filename = "redis.json"

configs = load_config(filename)

if 'tag' in configs:
    tag = configs['tag']
else:
    tag = f'{ randint(0, 100) }'


class RedisClient(object):
    def __init__(self, host=configs['redis_host'], port=configs['redis_port'], pw=configs['redis_password'], cert=configs['redis_cert']):
        self.rc = redis.StrictRedis(host=host, port=port, password=pw, ssl=True, ssl_certfile=cert, ssl_cert_reqs=None, ssl_check_hostname=False)

    
    def query(self, key, command='GET', name=None):
        """Function to Test GET operation on Redis"""
        if not name:
            name = key
        result = None
        start_time = time.time()
        try:
            result = self.rc.get(key)
            if not result:
                result = ''
        except Exception as e:
            total_time = round((time.time() - start_time) * 1000, 2)
            events.request_failure.fire(request_type=command, name=name, response_time=total_time, response_length=0, exception=e)
        else:
            total_time = round((time.time() - start_time) * 1000, 2)
            length = len(result)
            events.request_success.fire(request_type=command, name=name, response_time=total_time, response_length=length)
        return result

    def write(self, key, value, command='SET', name=None):
        """Function to Test SET operation on Redis"""
        if not name:
            name = key
        result = None
        start_time = time.time()
        try:
            result = self.rc.set(key,value)
            if not result:
                result = ''
        except Exception as e:
            total_time = round((time.time() - start_time) * 1000, 2)
            events.request_failure.fire(request_type=command, name=name, response_time=total_time, response_length=0, exception=e)
        else:
            total_time = round((time.time() - start_time) * 1000, 2)
            length = len(key) + len(value)
            events.request_success.fire(request_type=command, name=name, response_time=total_time, response_length=length)
        return result

    def execute(self, name, *args):
        """Function to execute some operation on Redis"""
        result = None
        start_time = time.time()
        try:
            result = self.rc.execute_command(*args)
            if not result:
                result = ''
        except Exception as e:
            total_time = round((time.time() - start_time) * 1000, 2)
            events.request_failure.fire(request_type=args[0], name=name, response_time=total_time, response_length=0, exception=e)
        else:
            total_time = round((time.time() - start_time) * 1000, 2)
            if type(result) == type(''):
                length = len(result)
            else:
                length = 1
            events.request_success.fire(request_type=args[0], name=name, response_time=total_time, response_length=length)
        return result

    def execute_pipeline(self, name, pipe):
        """Function to execute a pipeline of operations on Redis"""
        result = None
        start_time = time.time()
        try:
            result = pipe.execute()
            if not result:
                result = ''
        except Exception as e:
            total_time = round((time.time() - start_time) * 1000, 2)
            events.request_failure.fire(request_type='pipeline', name=name, response_time=total_time, response_length=0, exception=e)
        else:
            total_time = round((time.time() - start_time) * 1000, 2)
            length = 0
            for item in result:
               if type(item) == type(''):
                   length += len(item) 
               else:
                   length += 1
            events.request_success.fire(request_type='pipeline', name=name, response_time=total_time, response_length=length)
        return result



class RedisLocustRpushTest(User):
    def __init__(self, *args, **kwargs):
        super(RedisLocustRpushTest, self).__init__(*args, **kwargs)
        self.client = RedisClient()

    wait_time = constant(0.01)

    @task
    def rpush_test(self):
        key = f'mylist:{{{ tag }}}'
        val = f'{ randint(1, 100000000) }'
        self.client.execute('rpush_test', 'RPUSH', key, val)
