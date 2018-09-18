from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, SmallInteger
from datetime import datetime

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__ (self):
        self.create_time = int(datetime.now().timestamp())

    def create_datetime (self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete (self):
        self.status = 0

    def set_attrs (self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)


from flaskr.models.user import *
