from abc import ABC, abstractmethod
from typing import Dict


class BaseOAuth(ABC):

    @abstractmethod
    def get_token(self) -> Dict:
        pass

    @abstractmethod
    def init(self, *, client_id, client_secret, code, redirect_uri) -> None:
        pass

    @abstractmethod
    def refresh_token(self) -> Dict:
        pass
