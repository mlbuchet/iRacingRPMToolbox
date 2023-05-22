"""
iRacing API Client

Simple iRacing API wrapper.

Usage:
client = irApiClient("user", "pwd")
data = client.request("league/season_sessions", league_id=7826, season_id=79984)
"""
import requests
import hashlib
import base64
import json

class irApiClient:
    def __init__(self, username=None, password=None):
        self.authenticated = False
        self.session = requests.Session()
        self.base_url = "https://members-ng.iracing.com"
        self.auth_path = "/auth"
        self.introspect_path = "/data/doc"

        self._login(username=username, password=password)
        self.introspect = self._http_get(self.introspect_path)

    def _login(self, username=None, password=None):
        if not username or not password:
            raise RuntimeError("Please supply a username and password")

        payload = {
            "email": username,
            "password": self._encode_pw(username, password)
        }

        r = self.session.post(self._build_url(self.auth_path), json=payload)
        if r.status_code != 200:
            raise RuntimeError("Error from iRacing: ", r.json())

        self.authenticated = True
        return True

    def _encode_pw(self, username, password):
        initialHash = hashlib.sha256((password + username.lower()).encode('utf-8')).digest()
        hashInBase64 = base64.b64encode(initialHash).decode('utf-8')
        return hashInBase64

    def _build_url(self, endpoint):
        '''
        Prepend base url if it's relative
        '''
        return endpoint if endpoint.startswith("http") else self.base_url + endpoint

    def _http_get(self, url, params={}):
        '''
        HTTP GET
        '''
        r = self.session.get(self._build_url(url), params=params)
        if r.status_code != 200:
            raise RuntimeError(r.json())
        return r.json()

    def _deep_get(self, d, keys, default=None):
        '''
        Safe deep get in a hash
        '''
        assert type(keys) is list
        if d is None:
            return default
        if not keys:
            return d
        return self._deep_get(d.get(keys[0]), keys[1:], default)

    def _get_endpoint(self, path):
        endpoint = self._deep_get(self.introspect, path.split('/'))
        if endpoint is None:
            raise RuntimeError("Endpoint not found: " + path)
        return endpoint

    def info(self, path, **kwargs):
        '''
        Prints information about an endpoint
        (**kwargs is here to match request() signature)
        '''
        endpoint = self._get_endpoint(path)
        print(json.dumps(endpoint, indent=4))

    def request(self, path, **kwargs):
        '''
        Validate endpoint and parameters against the doc and follow any links/chunks
        to get the data.

        Usage: r = request("results/get", subsession_id=46478758)
        '''
        endpoint = self._get_endpoint(path)

        # Validate parameters
        if "parameters" in endpoint:
            for key in endpoint["parameters"]:
                if "required" in endpoint["parameters"][key] and key not in kwargs:
                    raise RuntimeError("Missing mandatory parameter: " + key)

        res = self._http_get(endpoint["link"], params=kwargs)

        # Follow links
        if "link" in res:
            res = self._http_get(res["link"])

        # Get chunks
        if "chunk_info" in res:
            chunks = res["chunk_info"]
            base_url = chunks['base_download_url']
            urls = [base_url+x for x in chunks['chunk_file_names']]
            list_of_chunks = [self._http_get(url) for url in urls]
            res = [item for sublist in list_of_chunks for item in sublist]

        return res
