from abc import ABC, abstractmethod
from typing import Dict, Tuple


class _FlaskRequestType(ABC):

    base_url = None

    @staticmethod
    @abstractmethod
    def get_json() -> Dict:
        pass


class BaseOAuth(ABC):

    header_name: str

    tablename: str

    @abstractmethod
    def init(self, *, client_id, client_secret, redirect_uri, expires_in, email_field, tablename) -> None:
        pass

    @abstractmethod
    def oauth_login(self, request: _FlaskRequestType) -> Dict:
        pass

    @abstractmethod
    def authorize(self, token: str) -> Dict:
        pass


class TestBaseOAuth(BaseOAuth, ABC):
    test_metadata: Dict[str, Dict[str, str]] = {}

    @abstractmethod
    def create_test_headers(self, *, email: str, entity: object = None, scope: str = "function") -> Dict[str, str]:
        pass

    @abstractmethod
    def update_test_metadata(self, email: str) -> Tuple[str, object]:
        pass

    @abstractmethod
    def tear_down(self, *, scope: str = "function"):
        pass
