from nose.tools import ok_, eq_, raises

from . import BaseTest
import settings
from application import fb


class FBTest(BaseTest):

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
