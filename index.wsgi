# -*- coding:utf-8 -*-
import sae
import os
import sys

root = os.path.dirname(__file__)

# 两者取其一
sys.path.insert(0, os.path.join(root, 'site-packages'))
from nxxapp import app
from view.admin_views import admin
from view.blog_views import blog
from view.auth_views import auth

app.register_blueprint(admin)
app.register_blueprint(blog)
app.register_blueprint(auth)

application = sae.create_wsgi_app(app)
