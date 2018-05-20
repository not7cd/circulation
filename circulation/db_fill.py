# -*- coding: utf-8 -*-

from circulation.web import app, db
from circulation.models import User, Role

app_ctx = app.app_context()
app_ctx.push()
db.create_all()
Role.insert_roles()

admin = User(name=u'root', email='root@gmail.com', password='password')

db.session.add(admin)
db.session.commit()

app_ctx.pop()
