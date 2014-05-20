import json

from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

from application import db


class FBUser(db.Model):
    __table_args__ = {'useexisting': True}

    id = db.Column(db.Integer, primary_key=True)
    facebook_id = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(100), nullable=True)

    def add_and_commit(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        convert = dict()
        d = dict()
        for c in self.__class__.__table__.columns:
            v = getattr(self, c.name)
            if c.type in convert.keys() and v is not None:
                try:
                    d[c.name] = convert[c.type](v)
                except:
                    d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
            elif v is None:
                d[c.name] = str()
            else:
                d[c.name] = v

        return d

    def remove_and_commit(self):
        db.session.delete(self)
        db.session.commit()
