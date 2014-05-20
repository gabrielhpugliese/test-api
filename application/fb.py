import requests


GRAPH_URL = 'https://graph.facebook.com/v1.0/'


def get_user(facebook_id):
    return _get(facebook_id)


def _get(facebook_id):
    url = '{}{}'.format(GRAPH_URL, facebook_id)
    return requests.get(url).json()
