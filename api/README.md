
# Black Friday Scraper API

The Web App will use this API to retrive data from the Database. \
The API will be running at http://localhost:5000. \
All responses will be in `JSON` fromat.

## Start the API service

Run in main directory:
```
docker-compose up -d
```
After all the services are started and up to date, run:
```
docker-compose exec bf_api python ./bf_api.py
````

## Usage
`http://localhost:5000/api` - Will show this documentation in browser
### Information available in database

- Companies
- Products Types
- Products
- Products Prices

### Companies Data

**Definition**

- `GET api/companies` - List all companies

**Response**
```json
[
  {
    "name": "APPLE"
  },
  {
    "name": "SAMSUNG"
  }
]
```
### Porducts Types Data

**Definition**

- `GET api/types` - List all types.

**Response**
```json
[
  {
    "name": "iPhone Xs Max"
  },
  {
    "name": "iPhone 11 Pro Max"
  }
]
```
### Porducts

**Definitions**

- `GET api/products` - List just the name of products.
- `GET api/detailed/products` - List name, specifications, type, and company for all products.
- `GET api/detailed/products/<string:product_name>` - Search products by name and retrieve all the matches with detalied information.
- `GET api/detailed/products/<int:product_id>` - Search products by id and retrieve one product with detalied information.


**Response example**
For `http://localhost:5000/api/detailed/products/20` the response will be:
```json
[
  {
    "name": "iPhone SE 2",
    "company": "APPLE",
    "specifications": " 256GB,  White",
    "type": "Telefon"
  }
]
```
### Products Prices

**Definitions**

- `GET api/detailed/prices` - List name, specifications, company,  current price, old price (if the product is discounted) and the date when those prices were registered. This list contain the prices for all the products for all dates.
- `GET api/detailed/prices/<string:product_name>` - Search products by name and retrieve all the matches with detalied information about the prices.
- `GET api/detailed/prices/<int:product_id>` - Search prices by id of the record and retrieve one product with detalied information about prices.


**Response example**
For `http://localhost:5000/api/detailed/prices/galaxy-a41` the response will be:
```json
[
  {
    "name": "Galaxy A41",
    "company_name": "SAMSUNG",
    "specifications": " 64GB,  4GB RAM,  Dual SIM,  Prism Crush Black",
    "current_price": 1149.9,
    "old_price": 1399.9,
    "date": "Wed, 09 Sep 2020 10:25:37 GMT"
  },
  {
    "name": "Galaxy A41",
    "company_name": "SAMSUNG",
    "specifications": " 64GB,  4GB RAM,  Dual SIM,  Prism Crush Black",
    "current_price": 1149.9,
    "old_price": 1399.9,
    "date": "Thu, 10 Sep 2020 13:46:43 GMT"
  }
]
```
