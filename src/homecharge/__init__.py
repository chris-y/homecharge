import simplejson
import requests


def extract_value(data, path, default=None):
    paths = path.split('.')
    if len(paths) == 1:
        return data.get(paths[0], None)
    return extract_value(
        data.get(paths[0], {}),
        '.'.join(paths[1:])
    )


def requires_login(func):
    def inner(self, *args, **kwargs):
        if self._api_key is None:
            raise Exception("Nope")
        return func(self, *args, **kwargs)
    return inner


class Client(object):

    API_ROOT = 'https://api.chargevision.com/smart'
    AUTH_KEY = 'XLNAniZzLsGOtCqstsNgGzFquNuSICA5'

    def __init__(self, api_key=None):
        self._session = requests.Session()
        self._session.headers = {
            'Authorization': self.AUTH_KEY
        }

        self._api_key = api_key
        self._consumer = None
        self._chargepoint_data = None

    def login(self, email, password):
        data = self._session.post(
            '{}/login'.format(self.API_ROOT),
            {
                'email': email,
                'password': password
            }
        ).json()

        self._api_key = extract_value(data, 'data.consumer.apikey')

        login_data = extract_value(data, 'data')

        self._consumer = login_data.pop('consumer')
        self._chargepoint_data = login_data

        return self._api_key

    @property
    @requires_login
    def chargepoint(self):
        return self._chargepoint_data

    @property
    @requires_login
    def consumer(self):
        return self._consumer
