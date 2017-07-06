# -*- coding=utf-8 -*-
__author__ = 'zero'
import os
# import sae.const

# MYSQLDB配置信息
# MYSQL_USER = 'root'
# MYSQL_PASS = 'Dtt123456'
# MYSQL_HOST_M = '127.0.0.1'
# MYSQL_HOST_S = '127.0.0.1'
# MYSQL_PORT = '3306'
# MYSQL_DB = 'nxx'

TEMPLATE_FOLDER = 'templates'
STATIC_PATH = 'static'
UPLOAD_FOLDER = 'uploads'
ORI_IMAGES_FOLDER = 'uploads'+os.sep+'ori'
DST_IMAGES_FOLDER = 'uploads'+os.sep+'dst'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# configure our database for peewee
DATABASE = {
    'name': 'nxx',
    'engine': 'peewee.MySQLDatabase',
    'user': 'root',
    'passwd': 'Dtt123456',
    'charset': 'utf8'
}

Debug = True
CSRF_ENABLED = True
SECRET_KEY = 'niuxiaoxiao'
