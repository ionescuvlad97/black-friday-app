# Standard library imports

# Third party imports
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy_utils import create_view
from sqlalchemy import select

# Local application imports
from dbmodels.base import Base
from dbmodels.product import Product
from dbmodels.company import Company
from dbmodels.producttype import ProductType
from dbmodels.price import Price


stmt = select([
    Product.name.label('name'),
    Product.specifications,
    Company.name.label('company'),
    Price.current_price,
    Price.old_price,
    Price.date
]).select_from(Price.__table__.outerjoin(Product, Price.product_id == Product.id).outerjoin(Company, Company.id == Product.company_id))

# attaches the view to the metadata using the select statement
view = create_view('price_view', stmt, Base.metadata)

class PriceView(Base):
    __table__ = view
