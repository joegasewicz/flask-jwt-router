from http.client import HTTPResponse, HTTPException
import http.client
from typing import Dict, Union
import logging
import json


class HttpRequests:

    logger = logging.getLogger()

    def _get_headers(self, token: str) -> Dict[str, str]:
        t = {"Authorization": f"Bearer {token}"} if token else {}
        return {
            **t,
            "Content-type": "application/x-www-form-urlencoded",
        }

    def post_token(self, url: str, token: str = None) -> Union[Dict, None]:
        try:
            conn = http.client.HTTPConnection(url)
            conn.request("POST", "", None, self._get_headers(token))
            response = conn.getresponse()
            data = response.read()
            self.logger.debug(f"Successfully authenticated from {url}")
            assert 200 == response.status
            conn.close()
            return json.loads(data)
        except HTTPException as err:
            self.logger.debug(err, exc_info=True)

    def get_by_scope(self, scope_url: str, access_token: str = None) -> None:
        try:
            conn = http.client.HTTPConnection(scope_url)
            conn.request("GET", "", None, self._get_headers(access_token))
            response = conn.getresponse()
            assert 200 == response.status
            self.logger.debug(f"Successfully authenticated from {scope_url}")
        except HTTPException as err:
            self.logger.debug(err, exc_info=True)
