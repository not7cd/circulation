# -*- coding:utf-8 -*-
from app import db
from app.models import User
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import ValidationError
from wtforms.validators import Email, Length, DataRequired, EqualTo


class LoginForm(Form):
    email = StringField('Email',
                        validators=[DataRequired(message=u"Required field"), Length(1, 64), Email(message=u"Check Email address")])
    password = PasswordField(u'Password', validators=[DataRequired(message=u"Required field"), Length(6, 32)])
    remember_me = BooleanField(u"Keep me logged in.", default=True)
    submit = SubmitField(u'Log in')


class RegistrationForm(Form):
    email = StringField('Email',
                        validators=[DataRequired(message=u"Required field"), Length(1, 64), Email(message=u"Check Email address")])
    name = StringField(u'User name', validators=[DataRequired(message=u"Required field"), Length(1, 64)])
    password = PasswordField(u'Password',
                             validators=[DataRequired(message=u"Required field"), EqualTo('password2', message=u'Password must match.'),
                                         Length(6, 32)])
    password2 = PasswordField(u'Reconfirm Password', validators=[DataRequired(message=u"Required field")])
    submit = SubmitField(u'Register')

    def validate_email(self, field):
        if User.query.filter(db.func.lower(User.email) == db.func.lower(field.data)).first():
            raise ValidationError(u'This Email is already registered')


class ChangePasswordForm(Form):
    old_password = PasswordField(u'Old password', validators=[DataRequired(message=u"Required field")])
    new_password = PasswordField(u'New password', validators=[DataRequired(message=u"Required field"),
                                                     EqualTo('Confirm_password', message=u'Password must match'),
                                                     Length(6, 32)])
    confirm_password = PasswordField(u'Confirm new password', validators=[DataRequired(message=u"Required field")])
    submit = SubmitField(u"Save password")

    def validate_old_password(self, field):
        from flask.ext.login import current_user
        if not current_user.verify_password(field.data):
            raise ValidationError(u'Original password incorrect')
