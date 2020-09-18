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

class RedisClient(object):
    def __init__(self, host=configs['redis_host'], port=configs['redis_port'], pw=configs['redis_password'], cert=configs['redis_cert']):
        self.rc = redis.StrictRedis(host=host, port=port, password=pw, ssl=True, ssl_certfile=cert, ssl_cert_reqs=None, ssl_check_hostname=False)

    
    def query(self, key, command='GET'):
        """Function to Test GET operation on Redis"""
        result = None
        start_time = time.time()
        try:
            result = self.rc.get(key)
            if not result:
                result = ''
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type=command, name=key, response_time=total_time, response_length=0, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = len(result)
            events.request_success.fire(request_type=command, name=key, response_time=total_time, response_length=length)
        return result

    def write(self, key, value, command='SET'):
        """Function to Test SET operation on Redis"""
        result = None
        start_time = time.time()
        try:
            result=self.rc.set(key,value)
            if not result:
                result = ''
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type=command, name=key, response_time=total_time, response_length=0, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = 1
            events.request_success.fire(request_type=command, name=key, response_time=total_time, response_length=length)
        return result

    def execute(self, *args):
        """Function to Test SET operation on Redis"""
        result = None
        start_time = time.time()
        try:
            result=self.rc.execute_command(*args)
            if not result:
                result = ''
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type=args[0], name=args[0], response_time=total_time, response_length=0, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = 1
            events.request_success.fire(request_type=args[0], name=args[0], response_time=total_time, response_length=length)
        return result


class RedisLocust(User):
    def __init__(self, *args, **kwargs):
        super(RedisLocust, self).__init__(*args, **kwargs)
        self.client = RedisClient()

    wait_time = constant(0)

    @task
    def get_ping_time(self):
        self.client.execute('PING')

    @task
    def get_ping_message_time(self):
        self.client.execute('PING', 'ping with a message')
 
