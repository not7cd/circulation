# -*- coding:utf-8 -*-
from app.models import Book
from flask.ext.pagedown.fields import PageDownField
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms import ValidationError
from wtforms.validators import Length, DataRequired, Regexp


class EditBookForm(Form):
    isbn = StringField(u"ISBN",
                       validators=[DataRequired(message=u"Required field"),
                                   Regexp('[0-9]{13,13}', message=u"ISBN must be 13 digits")])
    title = StringField(u"Book title",
                        validators=[DataRequired(message=u"Required field"), Length(1, 128, message=u"Up to 128 characters")])
    origin_title = StringField(u"Original title", validators=[Length(0, 128, message=u"Up to 128 characters")])
    subtitle = StringField(u"Subtitle", validators=[Length(0, 128, message=u"Up to 128 characters")])
    author = StringField(u"Author", validators=[Length(0, 128, message=u"Up to 64 characters")])
    translator = StringField(u"Translator",
                             validators=[Length(0, 64, message=u"Up to 64 characters")])
    publisher = StringField(u"Publisher", validators=[Length(0, 64, message=u"Up to 64 characters")])
    image = StringField(u"Image location", validators=[Length(0, 128, message=u"Up to 128 characters")])
    pubdate = StringField(u"Publication date", validators=[Length(0, 32, message=u"Up to 32 characters")])
    tags = StringField(u"Tags", validators=[Length(0, 128, message=u"Up to 128 characters")])
    pages = IntegerField(u"Pages")
    price = StringField(u"Price", validators=[Length(0, 64, message=u"Up to 32 characters")])
    binding = StringField(u"Binding", validators=[Length(0, 16, message=u"Up to 16 characters")])
    numbers = IntegerField(u"Collection", validators=[DataRequired(message=u"Required field")])
    summary = PageDownField(u"Description")
    catalog = PageDownField(u"Contents")
    submit = SubmitField(u"Save changes")


class AddBookForm(EditBookForm):
    def validate_isbn(self, filed):
        if Book.query.filter_by(isbn=filed.data).count():
            raise ValidationError(u'A book with the same ISBN number already exists. Check whether or not the book has already been entered.')


class SearchForm(Form):
    search = StringField(validators=[DataRequired()])
    submit = SubmitField(u"Search")
