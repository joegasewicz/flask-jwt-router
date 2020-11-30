import urllib.request
from urllib.error import HTTPError, URLError, ContentTooShortError
from typing import Dict, Tuple
import logging
import json


class HttpRequests:

    logger = logging.getLogger()

    urls: Dict

    headers: Dict[str, str]

    def __init__(self, urls):
        self.urls = urls

    def get_url(self, name: str) -> str:
        return self.urls[name]

    def _get_headers(self, token: str = None) -> Dict[str, str]:
        t = {"Authorization": f"Bearer {token}"} if token else {}
        return {
            **t,
            "Content-type": "application/x-www-form-urlencoded",
        }

    def token(self, url: str, verb: str = "POST", data=None) -> Dict:
        try:
            req = urllib.request.Request(
                url=url,
                data=data,
                method=verb,
                headers=self._get_headers(),
            )
            with urllib.request.urlopen(req) as response:
                data = response.read().decode("utf-8")
            assert 200 == response.status
            self.logger.debug(f"Successfully authenticated from {url}")
            return json.loads(data)
        except HTTPError as err:
            self.logger.debug(err, exc_info=True)
        except ContentTooShortError as err:
            self.logger.debug(err, exc_info=True)
        except URLError as err:
            self.logger.debug(err, exc_info=True)
        # except AssertionError as err: TODO - move this to _routing.py
        #     self.logger.debug(err, exc_info=True)

    def get_by_scope(self, url: str, token, *, verb="GET", data=None) -> Dict:
        try:
            self.headers = self._get_headers(token)
            req = urllib.request.Request(
                url=url,
                data=data,
                method=verb,
                headers=self.headers,
            )
            with urllib.request.urlopen(req) as response:
                data = response.read().decode("utf-8")
            assert 200 == response.status
            self.logger.debug(f"Successfully authenticated from {url}")
            return json.loads(data)
        except HTTPError as err:
            self.logger.debug(err, exc_info=True)
        except ContentTooShortError as err:
            self.logger.debug(err, exc_info=True)
        except URLError as err:
            self.logger.debug(err, exc_info=True)
