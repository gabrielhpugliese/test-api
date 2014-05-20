import random

from flask.ext.testing import TestCase
from faker import Faker

from application import db, app, fb
from application.models import FBUser


class BaseTest(TestCase):

    render_templates = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()
        self.faker = Faker()
        self.faker.gender = lambda: random.choice(['male', 'female', None])
        self.faker.facebook_id = lambda: random.randint(1, 10000000000)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def insert_fixture(self, limit=1):
        facebook_id = self.faker.facebook_id()
        users = []

        for _ in range(limit):
            user = FBUser(
                facebook_id=str(facebook_id),
                name=self.faker.name(),
                username=self.faker.username(),
                gender=self.faker.gender()
            )
            user.add_and_commit()
            users.append(user)
            # increment one instead of random to not have conflict
            facebook_id += 1

        return users
