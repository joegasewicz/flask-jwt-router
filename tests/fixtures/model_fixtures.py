import pytest
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


class MockQuery:

    def __init__(self):
        self.results = [(1, u'joe')]

    def filter_by(self, **kwargs):
        return self

    def one(self):
        return self.results


@pytest.fixture
def TestMockEntity():
    Base = declarative_base()

    class TestEntity(Base):
        __tablename__ = "test_entity"

        query = MockQuery()

        id = Column(Integer(), primary_key=True)
        user_name = Column(String(10))

        def get_id_from_token(self, t):
            return [(1, u'joe')]
    return TestEntity


@pytest.fixture
def MockEntityModel():
    Base = declarative_base()
    class TestEntity(Base):
        __tablename__ = "test_entity"
        query = MockQuery()
        id = Column(Integer(), primary_key=True)
        user_name = Column(String(10))

    return TestEntity
