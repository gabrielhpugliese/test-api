from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api

import settings


def config_db(app):
    db = SQLAlchemy(app)

    for key, val in settings.DB.iteritems():
        app.config[key] = val

    return db


def config_route_map(api):
    import views
    api.add_resource(views.Person, '/person/')
    api.add_resource(views.PersonDelete, '/person/<string:facebook_id>/')


app = Flask(__name__)
api = Api(app)
db = config_db(app)

config_route_map(api)
app.config['DEBUG'] = settings.DEBUG
db.create_all()
