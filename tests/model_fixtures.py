import pytest
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


@pytest.fixture
def TestEntity():
    Base = declarative_base()

    class TestEntity(Base):
        __tablename__ = "test_entity"

        id = Column(Integer(), primary_key=True)
        user_name = Column(String(10))

        def get_id_from_token(self, t):
            return 1
    return TestEntity

