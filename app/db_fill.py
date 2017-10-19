# -*- coding: utf-8 -*-

from app import app, db
from app.models import User, Role

app_ctx = app.app_context()
app_ctx.push()
db.create_all()
Role.insert_roles()

admin = User(name=u'root', email='root@gmail.com', password='password')

db.session.add(admin)
db.session.commit()

app_ctx.pop()
