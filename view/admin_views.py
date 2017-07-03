# -*- coding:utf-8 -*-
__author__ = 'lilin'

from flask import render_template, request, redirect, url_for, session, flash, Blueprint
from model.user import User
from model.article import Article
from model.photo import Photo
from flask_login import login_required

admin = Blueprint('admin', __name__, url_prefix='/admin')


# Create tables
@admin.route('/init')
@login_required
def init():
    User.create_table(fail_silently=True)
    Article.create_table(fail_silently=True)
    Photo.create_table(fail_silently=True)
    users = User.select()
    return render_template('admin/admin.html', users=users, message='Init Success')
    # return redirect(url_for('admin.users'))


@admin.route('/')
@admin.route('/users')
@login_required
def users():
    users = User.select()
    return render_template('admin/admin.html', users=users)


@admin.errorhandler(404)
def page_not_found(error):
    return render_template('admin/page_not_found.html'), 404


@admin.errorhandler(401)
def page_not_found(error):
    return render_template('admin/page_not_found.html'), 401
