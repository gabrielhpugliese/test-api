import json
import random

from flask.ext.testing import TestCase
from nose.tools import ok_, eq_, raises
from faker import Faker

import settings
from application.models import FBUser
from application import db, app


class BaseViewTest(TestCase):

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


class TestPostView(BaseViewTest):

    def test_post_request_without_data(self):
        response = self.client.post('/person/')
        eq_(response.status_code, 400)
        data = json.loads(response.data)
        ok_('error' in data)
        eq_(data['code'], 100)

    def test_post_request_with_invalid_data(self):
        response = self.client.post('/person/', data={'googleId': 1234})
        eq_(response.status_code, 400)
        data = json.loads(response.data)
        ok_('error' in data)
        eq_(data['code'], 100)

    def test_post_request_with_valid_data(self):
        # my facebook id :)
        response = self.client.post('/person/', data={'facebookId': 1352586646})
        eq_(response.status_code, 201)
        data = json.loads(response.data)
        ok_('result' in data)

    def test_post_request_with_invalid_facebookId(self):
        response = self.client.post('/person/', data={'facebookId': -1})
        eq_(response.status_code, 500)
        data = json.loads(response.data)
        ok_('error' in data)
        eq_(data['code'], 500)


class TestGetView(BaseViewTest):

    def test_get_request_without_params(self):
        response = self.client.get('/person/')
        eq_(response.status_code, 400)
        data = json.loads(response.data)
        ok_('error' in data)
        eq_(data['code'], 200)

    def test_get_request_with_invalid_param(self):
        response = self.client.get('/person/?facebookId=12345')
        eq_(response.status_code, 400)
        data = json.loads(response.data)
        ok_('error' in data)
        eq_(data['code'], 200)

    def test_get_request_with_limit_one(self):
        limit = 1
        self.insert_fixture(limit)

        response = self.client.get('/person/?limit={}'.format(limit))
        eq_(response.status_code, 200)
        data = json.loads(response.data)
        ok_('result' in data)
        eq_(len(data['result']), 1)

    def test_get_request_with_limit_two(self):
        limit = 2
        self.insert_fixture(limit)

        response = self.client.get('/person/?limit={}'.format(limit))
        eq_(response.status_code, 200)
        data = json.loads(response.data)
        ok_('result' in data)
        eq_(len(data['result']), 2)
        
    def test_get_request_with_limit_ten(self):
        limit = 10
        self.insert_fixture(limit)

        response = self.client.get('/person/?limit={}'.format(limit))
        eq_(response.status_code, 200)
        data = json.loads(response.data)
        ok_('result' in data)
        eq_(len(data['result']), 10)


class TestDeleteView(BaseViewTest):

    def test_delete_request_without_params(self):
        response = self.client.delete('/person/')
        eq_(response.status_code, 405)
        data = json.loads(response.data)
        ok_('message' in data)
        eq_(data['status'], 405)

    def test_delete_request_with_non_existant_id(self):
        response = self.client.delete('/person/{}/'.format(self.faker.facebook_id()))
        eq_(response.status_code, 404)
        data = json.loads(response.data)
        ok_('error' in data)
        eq_(data['code'], 301)

    def test_delete_request_with_valid_id(self):
        user = self.insert_fixture(1)[0]
        response = self.client.delete('/person/{}/'.format(user.facebook_id))
        eq_(response.status_code, 204)

