from abc import ABC, abstractmethod
from typing import Dict


class _FlaskRequestType(ABC):

    base_url = None

    @staticmethod
    @abstractmethod
    def get_json() -> Dict:
        pass


class BaseOAuth(ABC):

    @abstractmethod
    def init(self, *, client_id, client_secret, redirect_uri, expires_in, email_field, tablename) -> None:
        pass

    @abstractmethod
    def oauth_login(self, request: _FlaskRequestType) -> Dict:
        pass

    @abstractmethod
    def create_test_headers(self, *, email: str, entity: object = None, scope: str = "function") -> Dict[str, str]:
        pass
