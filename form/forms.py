# -*- coding:utf-8 -*-
from flask_wtf import Form
# from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, BooleanField, PasswordField, SubmitField, validators, ValidationError, SelectField, \
    TextAreaField, FileField
from model.user import User
import os


def email_check(form, field):
    u = User.select().where(User.email == field.data)
    if u is not None and u.count() > 0:
        raise ValidationError('Email already exists.')


class LoginForm(Form):
    openid = StringField('openid')
    email = StringField('Email Address',
                        validators=[validators.DataRequired(), validators.Email(), validators.Length(min=6, max=35)])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)
    submit = SubmitField('Submit')


class SignupForm(Form):
    email = StringField('Email Address', validators=
    [validators.DataRequired(), validators.Email(), validators.Length(min=6, max=35), email_check])
    password = PasswordField('New Password', validators=[validators.DataRequired(), validators.EqualTo('confirm',
                                                                                                       message='Passwords must match')])
    confirm = PasswordField('Repeat Password', validators=[validators.DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)
    accept_tos = BooleanField('I accept the TOS', default=False)
    submit = SubmitField('Submit')


class ArticleForm(Form):
    article_title = StringField('Article Title',
                                validators=[validators.DataRequired(), validators.Length(min=1, max=3000)])
    article_content = TextAreaField('Article Content',
                                    validators=[validators.DataRequired(), validators.Length(min=1, max=3000)])
    article_type = SelectField('Article Type',
                               choices=[('Life', 'Life'), ('Work', 'Work'), ('Travel', 'Travel')], coerce=str)
    # release_time = DateField('Release Time')
    submit = SubmitField('Submit')


ALLOWED_IMG_EXT = set(['png', 'jpg', 'jpeg', 'gif'])


def check_photo(form, field):
    if field.data:  # this line raises exception
        filename = field.data.filename
        ext = os.path.splitext(filename)[1].strip(".")
        if not ext.lower() in ALLOWED_IMG_EXT:
            raise validators.ValidationError('Has to be an image')
    else:
        raise validators.ValidationError('Please, provide an image')


class PhotoForm(Form):
    photo_title = StringField('Photo Title',
                              validators=[validators.DataRequired(), validators.Length(min=1, max=3000)])
    photo_description = TextAreaField('Photo Description',
                                      validators=[validators.DataRequired(), validators.Length(min=1, max=3000)])
    photo_file = FileField('Upload File', validators=[validators.DataRequired(), check_photo])
    submit = SubmitField('Submit')
