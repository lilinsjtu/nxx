# -*- coding:utf-8 -*-
__author__ = 'lilin'

from peewee import *
import datetime
from nxxapp import db


class BaseModel(db.Model):
    id = PrimaryKeyField()
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)