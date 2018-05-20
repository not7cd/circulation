from circulation.models import Library as model_Library
from flask import url_for
from flask.ext.restful import Resource, marshal_with
from . import api, parser, default_per_page
from .fields import library_fields, library_list


@api.route('/libraries/<int:library_id>/')
class Library(Resource):
    @marshal_with(library_fields)
    def get(self, user_id):
        library = model_Library.query.get_or_404(library_id)
        library.uri = url_for('api.library', library_id=library_id, _external=True)
        return library


@api.route('/libraries/')
class LibraryList(Resource):
    @marshal_with(library_list)
    def get(self):
        args = parser.parse_args()
        page = args['page'] or 1
        per_page = args['per_page'] or default_per_page
        pagination = model_Library.query.order_by(model_Library.id.desc()).paginate(page=page, per_page=per_page)
        items = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.librarylist', page=page - 1, per_page=per_page, _external=True)
        next = None
        if pagination.has_next:
            next = url_for('api.librarylist', page=page + 1, per_page=per_page, _external=True)
        return {
            'items': items,
            'prev': prev,
            'next': next,
            'total': pagination.total,
            'pages_count': pagination.pages,
            'current_page': pagination.page,
            'per_page': per_page
        }
