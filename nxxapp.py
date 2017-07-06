# -*- coding:utf-8 -*-
__author__ = 'lilin'

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, g, request, render_template
from flask_peewee.db import Database
import MySQLdb
import setting
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CsrfProtect
from flask_cache import Cache
from flask_login import LoginManager

app = Flask(__name__)
bootstrap = Bootstrap(app)
csrf = CsrfProtect()
csrf.init_app(app)
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'
login_manager.login_message = 'Login First'

# PEEWEE数据库配置，从配置文件DATABASE读取
app.config.from_object(__name__)
app.config.from_pyfile('setting.py')
db = Database(app)


# # MySQLDatabase
@app.before_request
def before_request():
    # MySQLdb way
    # g.db = MySQLdb.connect(setting.MYSQL_HOST_M, setting.MYSQL_USER, setting.MYSQL_PASS,
    #                        setting.MYSQL_DB, port=int(setting.MYSQL_PORT), charset='utf8')

    # flask-peewee way
    db.connect_db()


@app.teardown_request
def teardown_request(exception):
    try:
        # if hasattr(g, 'db'):
        #     g.db.close
        db.close_db(exception)
    except exception:
        print exception


@csrf.error_handler
def csrf_error(reason):
    print reason
    return render_template('csrf_error.html', reason=reason), 400


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.errorhandler(401)
def page_not_found(error):
    return render_template('page_not_found.html'), 401

import view
