# -*- coding:utf-8 -*-
from circulation.web import db
from circulation.models import Book, Log, Comment, Permission, Tag, book_tag
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user
from . import book
from .forms import SearchForm, EditBookForm, AddBookForm
from ..comment.forms import CommentForm
from ..decorators import admin_required, permission_required


@book.route('/')
def index():
    search_word = request.args.get('search', None)
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)

    the_books = Book.query
    if not current_user.can(Permission.UPDATE_BOOK_INFORMATION):
        the_books = Book.query.filter_by(hidden=0)

    if search_word:
        search_word = search_word.strip()
        the_books = the_books.filter(db.or_(
            Book.title.ilike(u"%%%s%%" % search_word), Book.authors.ilike(u"%%%s%%" % search_word), Book.isbn.ilike(
                u"%%%s%%" % search_word), Book.tags.any(Tag.name.ilike(u"%%%s%%" % search_word)), Book.subtitle.ilike(
                u"%%%s%%" % search_word))).outerjoin(Log).group_by(Book.id).order_by(db.func.count(Log.id).desc())
        search_form.search.data = search_word
    else:
        the_books = Book.query.order_by(Book.id.desc())

    pagination = the_books.paginate(page, per_page=8)
    result_books = pagination.items
    return render_template("book.html", books=result_books, pagination=pagination, search_form=search_form,
                           title=u"List of Books")


@book.route('/<book_id>/')
def detail(book_id):
    the_book = Book.query.get_or_404(book_id)

    if the_book.hidden and (not current_user.is_authenticated or not current_user.is_administrator()):
        abort(404)

    show = request.args.get('show', 0, type=int)
    page = request.args.get('page', 1, type=int)
    form = CommentForm()

    if show in (1, 2):
        pagination = the_book.logs.filter_by(returned=show - 1) \
            .order_by(Log.borrow_timestamp.desc()).paginate(page, per_page=5)
    else:
        pagination = the_book.comments.filter_by(deleted=0) \
            .order_by(Comment.edit_timestamp.desc()).paginate(page, per_page=5)

    data = pagination.items
    return render_template("book_detail.html", book=the_book, data=data, pagination=pagination, form=form,
                           title=the_book.title)


@book.route('/<int:book_id>/edit/', methods=['GET', 'POST'])
@permission_required(Permission.UPDATE_BOOK_INFORMATION)
def edit(book_id):
    book = Book.query.get_or_404(book_id)
    form = EditBookForm()
    if form.validate_on_submit():
        book.isbn = form.isbn.data
        book.title = form.title.data
        book.subtitle = form.subtitle.data
        book.authors = form.authors.data
        book.translator = form.translator.data
        book.publisher = form.publisher.data
        book.thumbnail = form.thumbnail.data
        book.publishedDate = form.publishedDate.data
        book.tags_string = form.tags.data
        book.pageCount = form.pageCount.data
        book.numbers = form.numbers.data
        book.summary = form.summary.data
        db.session.add(book)
        db.session.commit()
        flash(u'Book information saved.', 'success')
        return redirect(url_for('book.detail', book_id=book_id))
    form.isbn.data = book.isbn
    form.title.data = book.title
    form.subtitle.data = book.subtitle
    form.authors.data = book.authors
    form.translator.data = book.translator
    form.publisher.data = book.publisher
    form.thumbnail.data = book.thumbnail
    form.publishedDate.data = book.publishedDate
    form.tags.data = book.tags_string
    form.pageCount.data = book.pageCount
    form.numbers.data = book.numbers
    form.summary.data = book.summary or ""
    return render_template("book_edit.html", form=form, book=book, title=u"Edit Book Information")


@book.route('/add/', methods=['GET', 'POST'])
@permission_required(Permission.ADD_BOOK)
def add():
    form = AddBookForm()
    if form.validate_on_submit():
        new_book = Book(
            isbn=form.isbn.data,
            title=form.title.data,
            subtitle=form.subtitle.data,
            authors=form.authors.data,
            translator=form.translator.data,
            publisher=form.publisher.data,
            thumbnail=form.thumbnail.data,
            publishedDate=form.publishedDate.data,
            tags_string=form.tags.data,
            pageCount=form.pageCount.data,
            numbers=form.numbers.data,
            summary=form.summary.data or "")
        db.session.add(new_book)
        db.session.commit()
        flash(u'%s sucessfully added' % new_book.title, 'success')
        return redirect(url_for('book.detail', book_id=new_book.id))
    return render_template("book_edit.html", form=form, title=u"Add New Book")


@book.route('/<int:book_id>/delete/')
@permission_required(Permission.DELETE_BOOK)
def delete(book_id):
    the_book = Book.query.get_or_404(book_id)
    the_book.hidden = 1
    db.session.add(the_book)
    db.session.commit()
    flash(u'Book record deleted.', 'info')
    return redirect(request.args.get('next') or url_for('book.detail', book_id=book_id))


@book.route('/<int:book_id>/put_back/')
@admin_required
def put_back(book_id):
    the_book = Book.query.get_or_404(book_id)
    the_book.hidden = 0
    db.session.add(the_book)
    db.session.commit()
    flash(u'Book record recovered', 'info')
    return redirect(request.args.get('next') or url_for('book.detail', book_id=book_id))


@book.route('/tags/')
def tags():
    search_tags = request.args.get('search', None)
    page = request.args.get('page', 1, type=int)
    the_tags = Tag.query.outerjoin(book_tag).group_by(book_tag.c.tag_id).order_by(
        db.func.count(book_tag.c.book_id).desc()).limit(30).all()
    search_form = SearchForm()
    search_form.search.data = search_tags

    data = None
    pagination = None

    if search_tags:
        tags_list = [s.strip() for s in search_tags.split(',') if len(s.strip()) > 0]
        if len(tags_list) > 0:
            the_books = Book.query
            if not current_user.can(Permission.UPDATE_BOOK_INFORMATION):
                the_books = Book.query.filter_by(hidden=0)
            the_books = the_books.filter(
                db.and_(*[Book.tags.any(Tag.name.ilike(word)) for word in tags_list])).outerjoin(Log).group_by(
                Book.id).order_by(db.func.count(Log.id).desc())
            pagination = the_books.paginate(page, per_page=8)
            data = pagination.items

    return render_template('book_tag.html', tags=the_tags, title='Tags', search_form=search_form, books=data,
                           pagination=pagination)
