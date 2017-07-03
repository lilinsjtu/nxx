__author__ = 'lilin'
from peewee import *
import basemodel
import user


class Photo(basemodel.BaseModel):
    owner = ForeignKeyField(user.User, related_name='photos')
    title = TextField()
    description = TextField()
    dst_url = TextField()
    ori_url = TextField()
    checked = BooleanField()

    class Meta:
        db_table = 't_photo'