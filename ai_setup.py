#!/usr/bin/env python

import redis
import csv
import redisai
import numpy as np
from ml2rt import load_model
from os import environ


def setup_ai():

        if environ.get('REDIS_SERVER') is not None:
           redis_server = environ.get('REDIS_SERVER')
        else:
           redis_server = 'localhost'

        if environ.get('REDIS_PORT') is not None:
           redis_port = int(environ.get('REDIS_PORT'))
        else:
           redis_port = 6379

        if environ.get('REDIS_PASSWORD') is not None:
           redis_password = environ.get('REDIS_PASSWORD')
        else:
           redis_password = ''

        # Setup Connections
        conn = redisai.Client(
                host=redis_server,
                port=redis_port,
                password=redis_password
        )
        rdb = redis.Redis(
                host=redis_server,
                port=redis_port,
                password=redis_password
        )


        # Load our model

        tf_model = load_model('./classifier_model.pb')
        profile_model = conn.modelset(
        'profile_model', 'tf', 'cpu',
        inputs=['x'], outputs=['Identity'], data=tf_model)

        # Load the data
        with open('./users.csv', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for row in csv_reader:
                        rdb.sadd("USERLIST", row['USER'])
                        rdb.hset(
                                "user:{}".format(row['USER']),
                                mapping = {k: v for k, v in row.items() if k != 'USER'}
                        )


if __name__ == "__main__":
    setup_ai()


