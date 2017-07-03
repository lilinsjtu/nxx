# -*- coding:utf-8 -*-
__author__ = 'lilin'

from flask import render_template, request, redirect, url_for, session, flash, make_response, Blueprint
# debug switch between web and local
from nxxapp import app, login_manager
from model.user import User
from form.forms import LoginForm, SignupForm
from flask_login import login_user, logout_user, current_user

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    print user_id
    user = User.get(User.id == int(user_id))
    return user


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        confirm = form.confirm.data
        if check_email(email):
            if password != "" and password == confirm:
                q = User.insert(email=email, password=password, phone='', checked=1, is_admin=False)
                q.execute()
                user = User.select().where(User.email == email, User.password == password)
                login_user(user[0], remember=True)
                resp = make_response(redirect(url_for('blog.index')))
                # session['user'] = email
                # if form.remember_me:
                #     resp.set_cookie('user', email)
                #     resp.set_cookie('passwd', password)
                return resp
        if 'email' not in form.errors:
            form.errors['email'] = ['Email already exists.']
        else:
            form.errors['email'].append('Email already exists.')
    print form.errors
    return render_template('signup-bootstrap.html', form=form)


# AJAX check email
@auth.route('/check', methods=['GET', 'POST'])
def check():
    if 'email' in request.form and request.form['email'] != '':
        u = User.select().where(User.email == request.form['email'])
        print 'u', u
        if u and u.count() > 0:
            return 'exist'
        else:
            return 'avaliable'
    else:
        return 'input'


# False = exists
def check_email(email):
    u = User.select().where(User.email == email)
    if u is not None and u.count() > 0:
        return False
    return True


# True = validation pass
def check_login(email, password):
    u = User.select().where(User.email == email, User.password == password)
    print u.count()
    if u is not None and u.count() > 0:
        return True
    return False


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if 'user_id' not in session:

        # print request.form.get('email')
        # print request.form.get('password')
        # email = request.form.get('email')
        # password = request.form.get('password')
        # if request.method == 'POST' and check_login(email, password):
        #     user = User.select().where(User.email == email, User.password == password)
        #     login_user(user[0], remember=True)
        #     return redirect(url_for('blog.index'))

        # form.validate_on_submit屏蔽了直接post username和password模拟登录的可能
        if request.method == 'POST' and form.validate_on_submit():
            print form.email.data, form.password.data, form.remember_me.data
            if check_login(form.email.data, form.password.data):
                email = form.email.data
                password = form.password.data
                user = User.select().where(User.email == email, User.password == password)
                print user, user[0]
                print current_user
                login_user(user[0], remember=True)
                print current_user
                resp = make_response(redirect(url_for('blog.index')))
                # session['user'] = email
                # if form.remember_me:
                #     resp.set_cookie('user', email)
                #     resp.set_cookie('passwd', password)
                return resp
            form.email.errors.append('Wrong email or password.')
            print form.email.errors
            # error = 'Wrong email or password.'
        return render_template('login-bootstrap.html', form=form)
    return redirect(url_for('blog.index'))


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    print current_user
    logout_user()
    print current_user
    resp = make_response(redirect(url_for('auth.login')))
    return resp
