# Standard library imports

# Third party imports
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func

# Local application imports
from dbmodels.base import engine, Base, Session, object_as_dict
from dbmodels.producttype import ProductType
from dbmodels.company import Company
from dbmodels.price import Price
from dbmodels.product import Product
from dbmodels.product_view import ProductView
from dbmodels.price_view import PriceView


# Base.metadata.create_all(engine)

# At this point running the following yields 0, as expected,
# indicating that the view has been constructed on the server
# engine.execute(select([func.count('*')], from_obj=ProductView)).scalar()
