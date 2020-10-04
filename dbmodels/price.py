# Standard library imports
import datetime

# Third party imports
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

# Local application imports
from dbmodels.base import Base


class Price(Base):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    current_price = Column(Float)
    old_price = Column(Float)
    date = Column(DateTime, default=datetime.datetime.utcnow())

    # product = relationship("Product")

    def __init__(self, product_id=None, current_price=None, old_price=None):
        self.product_id = product_id
        self.current_price = current_price
        self.old_price = old_price
