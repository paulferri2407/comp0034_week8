'''
A version of models.py that uses a reflection to map classes to existing database tables

To use this you need to remove db.create_all() from __init__.py and replace with:

    with app.app_context():
        db.Model.metadata.reflect(db.engine)

'''
from my_app import db


class User(db.Model):
    ''' deal with an existing table'''
    __table__ = db.Model.metadata.tables['db.user']
