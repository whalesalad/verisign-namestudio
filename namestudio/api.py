import json
import logging

import requests

from .utils import remove_empty

logger = logging.getLogger(__name__)


class NameStudioAPI(object):
    BASE_URL = "https://sugapi.verisign-grs.com/ns-api/2.0"

    DEFAULT_TIMEOUT_SECONDS = 5

    class NameStudioAPIError(Exception):
        def __init__(self, *args, request=None, response=None, **kwargs):
            self.request = request
            self.response = response
            super().__init__(*args, **kwargs)

    class HTTPTimeout(NameStudioAPIError):
        pass

    class OverQueryLimit(NameStudioAPIError):
        pass

    class UnknownError(NameStudioAPIError):
        pass

    def __init__(self, api_key, api_timeout=None):
        self.api_key = api_key
        self.api_timeout = int(api_timeout or self.DEFAULT_TIMEOUT_SECONDS)
        self.session = self.build_session()

    def build_session(self):
        session = requests.Session()
        session.headers = {
            'X-NAMESUGGESTION-APIKEY': self.api_key,
        }

        return session

    def get(self, url, params=None):
        try:
            response = self.session.get(
                f"{self.BASE_URL}{url}",
                params=remove_empty(params),
                timeout=self.api_timeout
            )

        except requests.ReadTimeout as e:
            raise self.HTTPTimeout() from e

        return self.parse_response(response)

    def parse_response(self, response):
        try:
            data = response.json()

        except json.decoder.JSONDecodeError as e:
            raise self.UnknownError(
                request=response.request,
                response=response
            ) from e

        error_code = data.get('code', None)
        error_message = data.get('message', None)

        if response.status_code == 429:
            if (error_code == 999) or (error_message == 'OVER_QUERY_LIMIT'):
                raise self.OverQueryLimit()

        return data, response

    def bulk_check(self, domains, tlds=None, include_registered=True):
        params = {
            'names': ','.join(domains),
            'include-registered': include_registered,
        }

        data, response = self.get("/bulk-check", params)

        try:
            return data['results'], response

        except KeyError as e:
            raise self.UnknownError(
                request=response.request,
                response=response
            ) from e
