# Standard library imports

# Third party imports
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Date
from sqlalchemy import ForeignKey

# Local application imports
from dbmodels.base import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    specifications = Column(String(255))

    type_id = Column(Integer, ForeignKey('types.id'))
    # product_type = relationship("ProductType")

    company_id = Column(Integer, ForeignKey('companies.id'))
    # company = relationship("Company")

    def __init__(self, name=None, specifications=None, type_id=None, company_id=None):
        self.name = name
        self.specifications = specifications
        self.type_id = type_id
        self.company_id = company_id
