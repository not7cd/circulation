import logging

from circulation.web import app, db
from circulation.models import User, Role

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('getting app context')
app_ctx = app.app_context()
app_ctx.push()

logger.info('create all tables')
db.create_all()
Role.insert_roles()

logger.info('create admin user')
admin = User(name=u'root', email='root@gmail.com', password='password')
db.session.add(admin)

logger.info('commit new db')
db.session.commit()

logger.info('close app context')
app_ctx.pop()
