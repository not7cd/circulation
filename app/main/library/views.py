# -*- coding:utf-8 -*-
from app import db
from app.models import User, Library, Log, Permission
from flask import render_template, url_for, flash, redirect, request, abort
from flask.ext.login import login_required, current_user
from . import library
from .forms import SearchForm, EditLibraryForm, AddLibraryForm
from ..decorators import admin_required, permission_required

@library.route('/')
@login_required
def index():
    search_word = request.args.get('search', None)
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)

    the_libraries = Library.query.order_by(Library.id.desc())

    pagination = the_libraries.paginate(page, per_page=8)
    result_libraries = pagination.items
    return render_template("library.html", libraries=result_libraries, pagination=pagination, search_form=search_form,
                           title=u"List of Libraries")


@library.route('/<int:library_id>/')
def detail(library_id):
    the_library = Library.query.get_or_404(library_id)

    show = request.args.get('show', 0, type=int)
    if show != 0:
        show = 1

    page = request.args.get('page', 1, type=int)
    pagination = the_library.logs.filter_by(returned=show) \
        .order_by(Log.borrow_timestamp.desc()).paginate(page, per_page=5)
    logs = pagination.items

    return render_template("library_detail.html", library=the_library, logs=logs, pagination=pagination,
                           title=u"Library Name: " + the_library.name)


@library.route('/<int:library_id>/edit/', methods=['GET', 'POST'])
def edit(library_id):
    library = Library.query.get_or_404(library_id)
    form = EditLibraryForm()
    if form.validate_on_submit():
        library.name = form.name.data
        library.address = form.address.data
        library.public = form.public.data

        db.session.add(library)
        db.session.commit()
        flash(u'Library information saved.', 'success')
        return redirect(url_for('library.detail', library_id=library_id))
    form.name.data = library.name
    form.address.data = library.address
    form.public.data = library.public
    return render_template("library_edit.html", form=form, library=library, title=u"Edit Library Information")


@library.route('/add/', methods=['GET', 'POST'])
def add():
    form = AddLibraryForm()
    if form.validate_on_submit():
        new_library = Library(
            name=form.name.data,
            address=form.address.data,
            public=form.public.data,
            user_id=current_user.id)
        db.session.add(new_library)
        db.session.commit()
        flash(u'%s sucessfully added' % new_library.name, 'success')
        return redirect(url_for('library.detail', library_id=new_library.id))
    return render_template("library_edit.html", form=form, title=u"Add New Library")


@library.route('/<int:library_id>/delete/')
@permission_required(Permission.DELETE_LIBRARY)
def delete(library_id):
    the_library = Library.query.get_or_404(library_id)
    the_library.hidden = 1
    db.session.add(the_library)
    db.session.commit()
    flash(u'Library record.', 'info')
    return redirect(request.args.get('next') or url_for('library.detail', library_id=library_id))


@library.route('/<int:library_id>/put_back/')
@admin_required
def put_back(library_id):
    the_library = Library.query.get_or_404(library_id)
    the_library.hidden = 0
    db.session.add(the_library)
    db.session.commit()
    flash(u'Library recovered', 'info')
    return redirect(request.args.get('next') or url_for('library.detail', library_id=library_id))
