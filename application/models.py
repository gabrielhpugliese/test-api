from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

from application import db


class FBUser(db.Model):
    __table_args__ = {'useexisting': True}

    id = db.Column(db.Integer, primary_key=True)
    facebook_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(100), nullable=True)

    def add_and_commit(self):
        db.session.add(self)
        db.session.commit()


@event.listens_for(FBUser, 'before_insert')
def check_facebook_id_type(mapper, connection, target, *args, **kwargs):
    if type(target.facebook_id) != int:
        raise IntegrityError('Facebook id cannot be other type than int', type(target.facebook_id), IntegrityError)

