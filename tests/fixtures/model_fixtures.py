import pytest
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


class MockQuery:

    def __init__(self):
        self.results = [(1, u'joe')]

    def filter_by(self, **kwargs):
        email = kwargs.get("email")
        if email:
            self.results = [(1, u'jaco@gmail.com')]
        return self

    def one(self):
        return self.results


@pytest.fixture
def TestMockEntity():
    Base = declarative_base()

    class TestEntity(Base):
        __tablename__ = "test_entities"

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
        __tablename__ = "test_entities"
        query = MockQuery()
        id = Column(Integer(), primary_key=True)
        user_name = Column(String(10))

    return TestEntity


@pytest.fixture
def MockEntityModelTwo():
    Base = declarative_base()
    class TestEntityTwo(Base):
        __tablename__ = "test_two_entities"
        query = MockQuery()
        id = Column(Integer(), primary_key=True)
        user_name = Column(String(10))

    return TestEntityTwo

@pytest.fixture
def MockEntityModelThree():
    Base = declarative_base()
    class TestEntityThree(Base):
        __tablename__ = "test_3_entities"
        query = MockQuery()
        teacher_id = Column(Integer(), primary_key=True)
        user_name = Column(String(10))

    return TestEntityThree


@pytest.fixture
def MockAOuthModel():
    Base = declarative_base()
    class TestOAuthModel(Base):
        __tablename__ = "oauth_tablename"
        query = MockQuery()
        id = Column(Integer(), primary_key=True)
        email = Column(String(20))

    return TestOAuthModel



@pytest.fixture
def NoTableNameEntity():
    Base = declarative_base()
    class TestEntityThree(Base):
        query = MockQuery()
        id = Column(Integer(), primary_key=True)
        user_name = Column(String(10))

    return TestEntityThree


