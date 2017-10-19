# -*- coding:utf-8 -*-
from app.models import Library
from flask.ext.pagedown.fields import PageDownField
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms import ValidationError
from wtforms.validators import Length, DataRequired, Regexp


class EditLibraryForm(Form):
    name = StringField(u"Library name",
                        validators=[DataRequired(message=u"Required field"), Length(1, 128, message=u"Up to 128 characters")])
    address = StringField(u"Address", validators=[Length(0, 128, message=u"Up to 128 characters")])
    public = BooleanField(u"Make public", default="checked")
    submit = SubmitField(u"Save")


class AddLibraryForm(EditLibraryForm):
    def validate_library(self, filed):
        if Library.query.filter_by(name=filed.data).count():
            raise ValidationError(u'A library with the same name already exists. Check whether or not the library has already been entered.')


class SearchForm(Form):
    search = StringField(validators=[DataRequired()])
    submit = SubmitField(u"Search")
