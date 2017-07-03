# -*- coding:utf-8 -*-
__author__ = 'lilin'
from peewee import *
import basemodel


class User(basemodel.BaseModel):
    email = TextField()
    password = TextField()
    phone = TextField()
    checked = IntegerField()
    is_admin = BooleanField()

    class Meta:
        db_table = 't_user'

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    # @staticmethod
    # def get(id):
    #     u = User.select().where(User.id == id)
    #     if u and u.count() > 0:
    #         return u[0]
    #     return None
