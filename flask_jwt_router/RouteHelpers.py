import jwt
from datetime import datetime
from dateutil.relativedelta import *

from .FlaskJwtRouter import FlaskJwtRouter


class RouteHelpers(FlaskJwtRouter):

    def __init__(self, app=None, **kwargs):
        super().__init__(app, **kwargs)
        self.app = self.get_app_config(app)

    def encode_jwt(self, **kwargs):
        """
        :param kwargs:
        :return: str
        """
        entity_key = self.get_entity_key()
        exp = self.get_exp(kwargs)
        secret_key = self.get_secret_key()

        if self.get_entity_id(kwargs):
            entity_id = self.get_entity_id(kwargs)
        else:
            raise KeyError("Entity id not in kwargs")

        encoded = jwt.encode({
            f"{entity_key}": entity_id,
            "exp": datetime.utcnow() + relativedelta(days=+exp)  # TODO options for different time types
        },
            secret_key,
            algorithm="HS256"
        ).decode("utf-8")
        return encoded

    def register_entity(self, **kwargs):
        """
        :param kwargs:
        :return: str
        """
        return self.encode_jwt(**kwargs)

    def update_entity(self, **kwargs):
        """
        :param kwargs:
        :return: str
        """
        return self.encode_jwt(**kwargs)
