from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import settings


def config_db(app):
    db = SQLAlchemy(app)

    for key, val in settings.DB.iteritems():
        app.config[key] = val

    return db


app = Flask(__name__)
app.config['DEBUG'] = settings.DEBUG

db = config_db(app)
