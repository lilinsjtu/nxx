__author__ = 'lilin'
from peewee import *
import basemodel
import user


class Article(basemodel.BaseModel):
    owner = ForeignKeyField(user.User, related_name='articles')
    title = TextField()
    content = TextField()
    article_type = TextField()
    author = TextField()
    release_time = DateField()
    checked = BooleanField()

    class Meta:
        db_table = 't_article'