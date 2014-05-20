from flask.ext.testing import TestCase
from nose.tools import ok_, eq_, raises
from faker import Faker

import settings
from application import db, app, fb


class BaseFBTest(TestCase):

    render_templates = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()
        self.faker = Faker()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FBTest(BaseFBTest):

    @raises(TypeError)
    def test_get_user_without_params(self):
        user = fb.get_user() 

    def test_get_user_with_valid_param(self):
        facebook_id = '1352586646'
        user = fb.get_user(facebook_id)

        ok_(user)
        eq_(user['id'], facebook_id)
        eq_(user['name'], 'Gabriel H Pugliese')
        eq_(user['username'], 'gabrielsapo')

    @raises(fb.FBError)
    def test_get_user_with_invalid_facebook_id(self):
        facebook_id = '1' * 15
        user = fb.get_user(facebook_id)
