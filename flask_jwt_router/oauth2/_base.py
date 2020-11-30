from abc import ABC, abstractmethod
from typing import Dict


class BaseOAuth(ABC):

    # @abstractmethod
    # def get_token(self) -> Dict:
    #     pass

    @abstractmethod
    def init(self, *, client_id, client_secret, redirect_uri, expires_in, email_field, tablename) -> None:
        pass

