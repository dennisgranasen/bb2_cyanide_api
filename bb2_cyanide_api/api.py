"""BB2 api agent modul"""
import requests
from .adapter import adapter

class BB2APINotAvailable(Exception):
  """Exception to raise for BB2API timeout issues"""

class Agent:
    DEFAULT_VERSION = 2
    DEFAULT_PLATFORM = 'pc'
    """BB2 api agent"""
    BASE_URL = "http://web.cyanide-studio.com/ws/bb2/"
    def __init__(self, api_key):
        self.api_key = api_key
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        self.http = http

    def team(self, name, **kwargs):
        """Pulls team data"""
        kwargs['name'] = name
        if 'platform' not in kwargs:
            kwargs['platform'] = self.DEFAULT_PLATFORM
        if 'bb' not in kwargs:
            kwargs['bb'] = self.DEFAULT_VERSION
        r = self.call("team", **kwargs)
        data = r.json()
        return data

    def match(self, id, **kwargs):
        """Pulls match id data"""
        kwargs['match_id'] = id
        #kwargs['id'] = id
        if 'bb' not in kwargs:
            kwargs['bb'] = self.DEFAULT_VERSION
        r = self.call("match", **kwargs)
        data = r.json()
        return data

    def league(self, name, **kwargs):
        """Pulls league data"""
        kwargs['league'] = name
        if 'platform' not in kwargs:
            kwargs['platform'] = self.DEFAULT_PLATFORM
        if 'bb' not in kwargs:
            kwargs['bb'] = self.DEFAULT_VERSION
        r = self.call("league", kwargs)
        data = r.json()
        return data

    def leagues(self, name, **kwargs):
        """Pulls leagues data"""
        kwargs['league'] = name
        if 'platform' not in kwargs:
            kwargs['platform'] = self.DEFAULT_PLATFORM
        if 'bb' not in kwargs:
            kwargs['bb'] = self.DEFAULT_VERSION
        if 'teams' not in kwargs:
            kwargs['teams'] = 0 # min no. registered teams
        if 'limit' not in kwargs:
            kwargs['limit'] = 100 # max no. leagues to return
        r = self.call("leagues", **kwargs)
        data = r.json()
        return data

    def competitions(self, leagues):
        """Pulls competitions data"""
        r = self.call("competitions", league=leagues)
        data = r.json()
        return data

    def contest(self, leagues):
        """Pulls competitions data"""
        r = self.call("competitions", league=leagues)
        data = r.json()
        return data

    def matches(self, **kwargs):
        """Pull matches"""
        if 'limit' not in kwargs:
            kwargs['limit'] = 10000
        if 'v' not in kwargs:
            kwargs['v'] = self.DEFAULT_VERSION
        if 'exact' not in kwargs:
            kwargs['exact'] = 0
        if 'start' not in kwargs:
            kwargs['start'] = '2016-01-01'
        r = self.call("matches", **kwargs)
        data = r.json()
        return data

    def call(self, method, **kwargs):
        """Call the api method with kwargs parameters"""
        url = self.__class__.BASE_URL + method+"/"
        kwargs['key'] = self.api_key
        kwargs['order'] = 'CreationDate'
        try: 
          return self.http.get(url=url, params=kwargs)
        except requests.exceptions.Timeout:
          raise BB2APINotAvailable("Service down")
