#!/usr/bin/env python
# -*- coding:utf -8-*-
import os

DEBUG = True

DATASET_DATABASE_URI = 'postgresql://awesome:awesome@127.0.0.1:5432/awesomedb'

# make the base dir to awesome
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# STATIC_FOLDER = os.path.join(BASE_DIR, 'www/')
# TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'static')

# Flask settings                     # Generated with: import os; os.urandom(24)
SECRET_KEY = '\x88\xaf\x90e\xc6D\xf5\xa5\x17\xcf\xd0Hc\x00!\xbfh\xc3\x06\xd2#\xe8s8'

APP_NAME = 'awesome'

#server address
SERVER_HOST = 'http://192.168.31.113:5000'

# for jsonify deal with chinese
JSON_AS_ASCII = False
