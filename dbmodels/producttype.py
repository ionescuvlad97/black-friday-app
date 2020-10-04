# Standard library imports

# Third party imports
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Date
from sqlalchemy import inspect

# Local application imports
from dbmodels.base import Base


class ProductType(Base):
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))

    def __init__(self, name=None):
        self.name = name
