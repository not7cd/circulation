from circulation.web import db
from circulation.models import User, Book, Comment, Log, Permission
from flask import render_template
from flask_login import current_user
from circulation.main.index import main
from circulation.main.book.forms import SearchForm


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@main.route('/')
def index():
    search_form = SearchForm()
    the_books = Book.query
    if not current_user.can(Permission.UPDATE_BOOK_INFORMATION):
        the_books = the_books.filter_by(hidden=0)
    popular_books = the_books.outerjoin(Log).group_by(Book.id).order_by(db.func.count(Log.id).desc()).limit(5)
    popular_users = User.query.outerjoin(Log).group_by(User.id).order_by(db.func.count(Log.id).desc()).limit(5)
    recently_comments = Comment.query.filter_by(deleted=0).order_by(Comment.edit_timestamp.desc()).limit(5)
    return render_template("index.html", books=popular_books, users=popular_users, recently_comments=recently_comments,
                           search_form=search_form)
