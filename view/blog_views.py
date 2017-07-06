# -*- coding:utf-8 -*-
__author__ = 'lilin'

from flask import render_template, request, Response, redirect, url_for, session, flash, send_from_directory, \
    make_response, Blueprint
from nxxapp import app
import random, time, datetime
from form.forms import ArticleForm, PhotoForm
from model.user import User
from model.article import Article
from model.photo import Photo
from werkzeug import secure_filename
import os
from PIL import Image
from handler.image_handler import *
from flask_login import login_required, current_user
from flask_paginate import Pagination
from nxxapp import cache

ISOTIMEFORMAT = '%Y-%m-%d %X'

blog = Blueprint('blog', __name__)


@blog.route('/')
@blog.route('/index')
@cache.cached(timeout=60)
def index():
    imgbaseurl = 'http://o93vhkh84.bkt.clouddn.com'
    prefix = '/image/marry/'
    dict = {}
    id = 10000
    now = time.strftime(ISOTIMEFORMAT, time.localtime())
    print now
    for num in range(1, 10):
        id += 1
        image = imgbaseurl + prefix + '0' + str(num) + '.jpg'
        dict[str(id)] = image

    for num in range(10, 62):
        id += 1
        image = imgbaseurl + prefix + str(num) + '.jpg'
        dict[str(id)] = image

    keys = random.sample(dict, len(dict))
    print len(dict)

    # 排序后return list，元素是tuple数组，采用[]取值
    list = sorted(dict.items(), key=lambda d: d[0])
    print list
    for l in list:
        print l[0], l[1]

    for (k, v) in dict.items():
        print "dict[%s] =" % k, v
    if request.cookies.get('email') and request.cookies.get('password'):
        email = request.cookies.get('email')
        password = request.cookies.get('password')
        users = User.select().where(User.email == email, User.password == password)
        if users.count() > 0:
            session['email'] = email
    return render_template('index.html', keys=keys, dict=dict, now=now)


@blog.route('/mood', methods=['GET', 'POST'])
@cache.cached(timeout=60)
@login_required
def mood():
    form = ArticleForm()
    articles = None
    print form.article_title.data, form.article_content.data
    print form.article_type.type, form.article_type.data
    if request.method == 'POST' and form.validate_on_submit():
        if 'user_id' in session:
            user = User.get(User.id == int(session['user_id']))
            q = Article.insert(owner=user, title=form.article_title.data, content=form.article_content.data,
                               article_type=form.article_type.data,
                               release_time=time.strftime(ISOTIMEFORMAT, time.localtime()), author=user.email,
                               checked=True)
            q.execute()
            return redirect(url_for('.mood'))
    # display articles
    pagination = None
    page = 1
    per_page = 10

    if 'user_id' in session:
        try:
            page = int(request.args.get('page', 1))
            if page == 0:
                page = 1
        except ValueError:
            page = 1
        search = True
        total = Article.select().where(Article.author == current_user.email)
        articles = Article.select().where(Article.author == current_user.email).order_by(
            Article.create_time.desc()).paginate(
            page,
            per_page)
        pagination = Pagination(page=page, per_page=per_page, found=total.count(),
                                total=total.count(), search=search, show_single_page=True,
                                record_name='articles', css_framework='bootstrap', bs_version=3)
    return render_template('mood.html', form=form, articles=articles, page=page, per_page=per_page,
                           pagination=pagination)


@blog.route('/photo', methods=['GET', 'POST'])
@cache.cached(timeout=60)
def photo():
    form = PhotoForm()
    photos = None
    print form.photo_title.data, form.photo_description.data
    print form.photo_file
    print form.photo_file.data
    print app.config['UPLOAD_FOLDER']
    # url = os.path.join(app.config['UPLOAD_FOLDER'],str(time.time()).replace('.','')+'.jpg')
    # print url
    if request.method == 'POST' and form.validate_on_submit():
        if 'user_id' in session and form.photo_file.data:
            user = User.get(User.id == int(session['user_id']))
            filename = form.photo_file.data.filename
            ext = os.path.splitext(filename)[1].strip(".")
            print filename, ext
            filename_pre = str(time.time()).replace('.', '')
            ori_img = os.path.join(app.config['ORI_IMAGES_FOLDER'], filename_pre + '_ori.' + ext)
            ori_url = ori_img.replace('\\', '/')
            print ori_img, ori_url
            # resize
            dst_img = os.path.join(app.config['DST_IMAGES_FOLDER'], filename_pre + '_dst.' + ext)
            dst_url = dst_img.replace('\\', '/')
            print dst_img, dst_url
            # on premise
            dst_w = 750
            dst_h = 750
            save_q = 75
            # Save storage
            # form.photo_file.data.save(ori_img)
            # resizeImg(ori_img=form.photo_file.data, dst_img=dst_img, dst_w=dst_w, dst_h=dst_h, save_q=save_q)
            # return redirect(url_for('uploads', filename=filename))
            q = Photo.insert(owner=user, title=form.photo_title.data, description=form.photo_description.data,
                             ori_url=ori_url, dst_url=dst_url,
                             checked=True)
            q.execute()
            return redirect(url_for('.photo'))
    print form.errors
    if 'user_id' in session:
        user = User.get(User.id == int(session['user_id']))
        photos = Photo.select(Photo, User).join(User).where(User.email == user.email).order_by(Photo.id.desc())
    return render_template('photo.html', form=form, photos=photos)


# open from directory
@blog.route('/uploads/<folder>/<filename>')
def uploaded_image(folder, filename):
    print folder, filename
    return send_from_directory("uploads" + os.sep + folder, filename)


@blog.route('/delete_article/<article_id>')
@login_required
def delete_article(article_id):
    q = Article.delete().where(Article.id == article_id)
    q.execute()
    return redirect(url_for('.mood'))


@blog.route('/travel')
def travel():
    return render_template('travel.html')


@blog.route('/theme')
def theme():
    return render_template('theme.html')


@blog.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@blog.errorhandler(401)
def page_not_found(error):
    return render_template('page_not_found.html'), 401
