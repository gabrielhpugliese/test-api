import json

from nose.tools import ok_, eq_, raises

from . import BaseTest
import settings


class TestPostView(BaseTest):

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

    def test_post_request_with_same_facebookId_two_times(self):
        response = self.client.post('/person/', data={'facebookId': 1352586646})
        response = self.client.post('/person/', data={'facebookId': 1352586646})
        eq_(response.status_code, 403)
        data = json.loads(response.data)
        ok_('error' in data)
        eq_(data['code'], 102)



class TestGetView(BaseTest):

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


class TestDeleteView(BaseTest):

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

