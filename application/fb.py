import requests


GRAPH_URL = 'https://graph.facebook.com/v1.0/'


class FBError(Exception):
    def __init__(self, message, error_type, code):
        self.message = message
        self.error_type = error_type
        self.code = code

    def __str__(self):
        return '{} (#{}): {}'.format(self.error_type, self.code, self.message)


def get_user(facebook_id):
    user = _get(facebook_id)
    if 'error' in user:
        error = user['error']
        raise FBError(error.get('message'), error.get('type'), error.get('code'))
    
    return user


def _get(facebook_id):
    url = '{}{}'.format(GRAPH_URL, facebook_id)
    return requests.get(url).json()
