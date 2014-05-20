import random

from flask.ext.testing import TestCase
from nose.tools import ok_, eq_, raises
from sqlalchemy.exc import IntegrityError
from faker import Faker

import settings
from application.models import FBUser
from application import db, app


class BaseModelTest(TestCase):

    render_templates = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        self.faker = Faker()
        self.faker.gender = lambda: random.choice(['male', 'female'])
        self.faker.facebook_id = lambda: random.randint(1, 10000000000)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestFBUser(BaseModelTest):

    @raises(IntegrityError)
    def test_create_blank_fbuser(self):
        fb_user = FBUser().add_and_commit()

    @raises(IntegrityError)
    def test_create_fbuser_without_facebook_id(self):
        FBUser(
            name=self.faker.name(),
            username=self.faker.username(),
            gender=self.faker.gender() 
        ).add_and_commit()

    @raises(IntegrityError)
    def test_create_fbuser_with_string_facebook_id(self):
        FBUser(
            facebook_id=self.faker.name(),
            name=self.faker.name(),
            username=self.faker.username(),
            gender=self.faker.gender() 
        ).add_and_commit()

    @raises(IntegrityError)
    def test_create_fbuser_with_negative_facebook_id(self):
        FBUser(
            facebook_id=-1,
            name=self.faker.name(),
            username=self.faker.username(),
            gender=self.faker.gender() 
        ).add_and_commit()

    @raises(IntegrityError)
    def test_create_fbuser_without_name(self):
        FBUser(
            facebook_id=self.faker.facebook_id(),
            username=self.faker.username(),
            gender=self.faker.gender()
        ).add_and_commit()

    @raises(IntegrityError)
    def test_create_fbuser_without_username(self):
        FBUser(
            facebook_id=self.faker.facebook_id(),
            name=self.faker.name(),
            gender=self.faker.gender()
        ).add_and_commit()

    def test_create_fbuser_without_gender(self):
        fbuser = FBUser(
            facebook_id=self.faker.facebook_id(),
            name=self.faker.name(),
            username=self.faker.username()
        )
        fbuser.add_and_commit()

        ok_(fbuser in db.session)

    def test_create_fbuser(self):
        fbuser = FBUser(
            facebook_id=self.faker.facebook_id(),
            name=self.faker.name(),
            username=self.faker.username(),
            gender=self.faker.gender()
        )
        fbuser.add_and_commit()

        ok_(fbuser in db.session)
