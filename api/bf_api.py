# Standard library imports
from collections import OrderedDict

# Third party imports
from flask import Flask
from flask import render_template
from flask import url_for
from flask import jsonify
from flask_restful import Api
from flask_restful import Resource
import markdown
from sqlalchemy import inspect

# Local application imports
from dbmodels.base import engine
from dbmodels.base import Base
from dbmodels.base import Session
from dbmodels.base import object_as_dict
from dbmodels.producttype import ProductType
from dbmodels.company import Company
from dbmodels.price import Price
from dbmodels.product import Product
from dbmodels.product_view import ProductView
from dbmodels.price_view import PriceView

# App configurations
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Api configurations
api = Api(app)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# API description page
@app.route('/api')
def info_api():
    with open('./README.md', 'r') as markdown_file:
        content = markdown_file.read()
        return markdown.markdown(content)

def select_all_query_to_json(obj):
    session = Session()
    result = [object_as_dict(response)
              for response in session.query(obj).all()]
    session.close()
    return jsonify(result)

def select_query_to_json(obj, *args):
    session = Session()

    result = [{column_name: column_value
                for column_name, column_value in zip(args, response)}
                for response in session.query(*[getattr(obj, arg)
                                                for arg in args]).all()]

    session.close()
    return jsonify(result)

def select_product_to_json(product_name):
    session = Session()

    product_name = ' '.join(product_name.split('-'))
    q = session.query(Product.name,
                      Company.name.label('company'),
                      Product.specifications,
                      ProductType.name.label('type')).\
                filter(Company.id == Product.company_id).\
                filter(ProductType.id == Product.type_id).\
                filter(Product.name.like('{}%'.format(product_name))).all()
    result = [{key: value for key, value in zip(elements.keys(), elements)} for elements in q]
    # result = [OrderedDict((key, val) for key, val in zip(elements.keys(), elements)) for elements in q]
    session.close()
    return jsonify(result)

def select_product_prices_to_json(product_name):
    session = Session()

    product_name = ' '.join(product_name.split('-'))
    q = session.query(Product.name,
                      Company.name.label('company_name'),
                      Product.specifications,
                      Price.current_price,
                      Price.old_price,
                      Price.date).\
                filter(Price.product_id == Product.id).\
                filter(Company.id == Product.company_id).\
                filter(Product.name.like('{}%'.format(product_name))).all()
    result = [{key: value for key, value in zip(elements.keys(), elements)} for elements in q]
    session.close()
    return jsonify(result)

def select_product_by_id(product_id):
    session = Session()

    q = session.query(Product.name,
                      Company.name.label('company'),
                      Product.specifications,
                      ProductType.name.label('type')).\
                filter(Company.id == Product.company_id).\
                filter(ProductType.id == Product.type_id).\
                filter(Product.id == product_id).all()
    result = [{key: value for key, value in zip(elements.keys(), elements)} for elements in q]
    session.close()
    return jsonify(result)

def select_product_prices_by_id(product_id):
    session = Session()
    q = session.query(Product.name,
                      Company.name.label('company_name'),
                      Product.specifications,
                      Price.current_price,
                      Price.old_price,
                      Price.date).\
                filter(Price.product_id == Product.id).\
                filter(Company.id == Product.company_id).\
                filter(Product.id == product_id).all()
    result = [{key: value for key, value in zip(elements.keys(), elements)} for elements in q]
    session.close()
    return jsonify(result)

# Detailed Resources Lists

class DetailedProductList(Resource):
    def get(self):
        return select_all_query_to_json(ProductView)

class DetailedPriceList(Resource):
    def get(self):
        return select_all_query_to_json(PriceView)

# Resources Lists

class TypeList(Resource):
    def get(self):
        return select_query_to_json(ProductType, 'name')

class CompanyList(Resource):
    def get(self):

        return select_query_to_json(Company, 'name')

class ProductList(Resource):
    def get(self):
        return select_query_to_json(Product, 'name')

# Specific Product/Products

class SpecificProduct(Resource):
    def get(self, product_name):
        return select_product_to_json(product_name)

class SpecificProductPrices(Resource):
    def get(self, product_name):
        return select_product_prices_to_json(product_name)

# Specific Product by id

class SpecificProductById(Resource):
    def get(self, product_id):
        return select_product_by_id(product_id)

class SpecificProductPricesByID(Resource):
    def get(self, product_id):
        return select_product_prices_by_id(product_id)


api.add_resource(TypeList, "/api/types")
api.add_resource(CompanyList, "/api/companies")
api.add_resource(ProductList, "/api/products")

api.add_resource(DetailedProductList, "/api/detailed/products")
api.add_resource(DetailedPriceList, "/api/detailed/prices")

api.add_resource(SpecificProduct, '/api/detailed/products/<string:product_name>')
api.add_resource(SpecificProductPrices, '/api/detailed/prices/<string:product_name>')

api.add_resource(SpecificProductById, '/api/detailed/products/<int:product_id>')
api.add_resource(SpecificProductPricesByID, '/api/detailed/prices/<int:product_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
