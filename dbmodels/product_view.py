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


stmt = select([
    Product.name.label('name'),
    Product.specifications,
    ProductType.name.label('type'),
    Company.name.label('company')
]).select_from(Product.__table__.outerjoin(ProductType, Product.type_id == ProductType.id).outerjoin(Company, Product.company_id == Company.id))

# attaches the view to the metadata using the select statement
view = create_view('product_view', stmt, Base.metadata)

class ProductView(Base):
    __table__ = view
