# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired, URL
from flask.ext.pagedown.fields import PageDownField
from flask.ext.wtf.file import FileField, FileAllowed
from circulation.web import avatars


class EditProfileForm(Form):
    name = StringField(u'User name', validators=[DataRequired(message=u"Required field"), Length(1, 64, message=u"Up to 64 characters")])
    major = StringField(u'Major', validators=[Length(0, 128, message=u"Up to 128 characters")])
    headline = StringField(u'About me (short)', validators=[Length(0, 32, message=u"Up to 32 characters")])
    about_me = PageDownField(u"About me")
    submit = SubmitField(u"Save")


class AvatarEditForm(Form):
    avatar_url = StringField('', validators=[Length(1, 100, message=u"Up to 100 characters"), URL(message=u"URL")])
    submit = SubmitField(u"Save")


class AvatarUploadForm(Form):
    avatar = FileField('', validators=[FileAllowed(avatars, message=u"Upload avatar image")])
