# -*- coding=utf-8 -*-
__author__ = 'lilin'
import os
import sys

root = os.path.dirname(__file__)

# 两者取其一
sys.path.insert(0, os.path.join(root, 'site-packages'))
from nxxapp import app
from model import user, article, photo

from view.admin_views import admin
from view.blog_views import blog
from view.auth_views import auth

app.register_blueprint(admin)
app.register_blueprint(blog)
app.register_blueprint(auth)

if __name__ == '__main__':
    # 初始化数据库
    user.User.create_table(fail_silently=True)
    article.Article.create_table(fail_silently=True)
    photo.Photo.create_table(fail_silently=True)
    app.debug = True
    app.run()
