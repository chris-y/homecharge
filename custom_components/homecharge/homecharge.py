from enum import Enum

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


class APIException(Exception):
    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data


class Period(Enum):
    ALL = 0
    LAST_SEVEN_DAYS = 1
    LAST_THIRTY_DAYS = 2
    LAST_THREE_MONTHS = 3
    LAST_SIX_MONTHS = 4


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
        self._session.headers['API-KEY'] = self._api_key

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

    @requires_login
    def _post(self, url, params={}, json=None):
        result = self._session.post(
            '{}/{}'.format(
                self.API_ROOT,
                url
            ),
            params=params,
            json=json
        )

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                data = result.json()
                msg = data.get('message')
                if msg:
                    raise APIException(result.status_code, msg, data)
                raise e
            except simplejson.JSONDecodeError:
                raise APIException(result.status_code, result.text)

        return result.json()['data']

    def get_dashboard(self, period=Period.LAST_SEVEN_DAYS):
        if not isinstance(period, Period):
            raise Exception('period should be a Period')

        return self._post(
            'dashboard',
            params={
                'when': period.value
            }
        )

    def get_charges(self, page=1):
        return self._post(
            'recharges',
            params={
                'page': page
            }
        )

    def override(self):
        '''Override schedule and charge immediately.'''
        return self._post(
            'override'
        )

    def get_schedule(self):
        schd = self._post(
            'schedule'
        ).get('schedule', [])

        return list(map(
            lambda s: ScheduledCharge.from_json(s),
            schd
        ))

    def save_schedule(self, schedule):
        if schedule._id:
            url = 'schedule/update'
        else:
            url = 'schedule/create'

        payload = {
            'schedule': schedule.for_json()
        }

        return self._post(
            url,
            json=payload
        )

    def delete_schedule(self, schedule):
        if schedule._id:
            return self._post(
                'schedule/delete',
                json={
                    'blockid': schedule._id
                }
            )


class DaysOfWeek(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class ScheduledCharge(object):
    def __init__(
        self,
        id=None,
        name=None,
        start_hour=None,
        start_minute=None,
        live=1,
        duration_hours=None,
        duration_minutes=None,
        max_charge='',
        days_of_week=[],
        power_level=3,
        fill_by=0
    ):
        self._id = id
        self.name = name
        self.start_hour = start_hour
        self.start_minute = start_minute
        self.live = live
        self.duration_hours = duration_hours
        self.duration_minutes = duration_minutes
        self.max_charge = max_charge
        self.days_of_week = days_of_week
        self.power_level = power_level
        self.fill_by = fill_by

    @staticmethod
    def from_json(j):
        return ScheduledCharge(
            id=j.get('blockid'),
            name=j.get('name'),
            start_hour=j.get('starthour'),
            start_minute=j.get('startmin'),
            live=j.get('live'),
            duration_hours=int(j.get('hrscharge')),
            duration_minutes=int(j.get('minscharge')),
            max_charge=j.get('maxkw'),
            days_of_week=list(map(lambda d: DaysOfWeek(d), j.get('days'))),
            power_level=j.get('chargelevel'),
            fill_by=j.get('fillmeby')
        )

    @property
    def duration(self):
        return (60 * self.duration_hours) + self.duration_minutes

    def for_json(self):
        data = {
            'name': self.name,
            'starthour': self.start_hour,
            'startmin': self.start_minute,
            'live': self.live,
            'hourscharge': self.duration_hours,
            'minscharge': self.duration_minutes,
            'maxkw': self.max_charge,
            'dow': list(map(lambda d: d.value, self.days_of_week)),
            'chargelevel': self.power_level,
            'fillmeby': self.fill_by
        }
        if self._id:
            data['blockid'] = self._id

        return data

    def __repr__(self):
        return '<ScheduledCharge {}: {}:{} for {} mins on {}>'.format(
            self.name,
            self.start_hour,
            self.start_minute,
            self.duration,
            ', '.join(list(map(lambda d: d.name, self.days_of_week)))
        )
