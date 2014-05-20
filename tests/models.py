from nose.tools import ok_, eq_, raises
from sqlalchemy.exc import IntegrityError

from . import BaseTest
from application.models import FBUser
from application import db


class TestFBUser(BaseTest):

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
