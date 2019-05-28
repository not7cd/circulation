# -*- coding:utf-8 -*-
from circulation.models import Book
from flask_pagedown.fields import PageDownField
from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms import ValidationError
from wtforms.validators import Length, DataRequired, Regexp, Optional


class EditBookForm(Form):
    isbn = StringField(u"ISBN (without hypens)",
                       validators=[DataRequired(message=u"Required field"),
                                   Regexp('[0-9]{13,13}', message=u"ISBN must be 13 digits")])
    title = StringField(u"Book Title",
                        validators=[DataRequired(message=u"Required field"), Length(1, 128, message=u"Up to 128 characters")])
    subtitle = StringField(u"Subtitle", validators=[Length(0, 128, message=u"Up to 128 characters")])
    authors = StringField(u"Authors", validators=[Length(0, 128, message=u"Up to 64 characters")])
    translator = StringField(u"Translator",
                             validators=[Length(0, 64, message=u"Up to 64 characters")])
    publisher = StringField(u"Publisher", validators=[Length(0, 64, message=u"Up to 64 characters")])
    thumbnail = StringField(u"Cover Image URL", validators=[Length(0, 128, message=u"Up to 128 characters")])
    publishedDate = StringField(u"Publication Date", validators=[Length(0, 32, message=u"Up to 32 characters")])
    tags = StringField(u"Tags", validators=[Length(0, 128, message=u"Up to 128 characters")])
    pageCount = IntegerField(u"Page Count", validators=[Optional()])
    numbers = IntegerField(u"Number of books in collection", validators=[DataRequired(message=u"Required field")])
    summary = PageDownField(u"Description")
    submit = SubmitField(u"Save")


class AddBookForm(EditBookForm):
    def validate_isbn(self, filed):
        if Book.query.filter_by(isbn=filed.data).count():
            raise ValidationError(u'A book with the same ISBN number already exists. Check whether or not the book has already been entered.')


class SearchForm(Form):
    search = StringField(validators=[DataRequired()])
    submit = SubmitField(u"Search")
