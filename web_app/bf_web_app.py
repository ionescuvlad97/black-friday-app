# Standard library imports
from collections import OrderedDict
import requests
# from urllib import request
import json
from collections import Counter, OrderedDict, defaultdict

# Third party imports
from flask import Flask
from flask import render_template
from flask import url_for
from flask import jsonify
import markdown
from pandas import DataFrame

# Local application imports


# App configurations
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Home page
@app.route('/')
def index():
    d = json.loads(requests.get('http://bf_api:5000/api/detailed/prices').content)
    product_number_by_company = OrderedCounter(elem['company'] for elem in d)
    company_avg_price_per_day = defaultdict(float)
    for elem in d:
        company_avg_price_per_day[(elem['company'], elem['date'])] += elem['current_price']
    # print(company_avg_price_per_day)
    df = DataFrame(d)
    print(dir(df.groupby(['company', 'date'])))
    print(df.groupby(['company', 'date']).company)

    r = requests.get('http://bf_api:5000/api/companies')
    data = json.loads(r.content)
    return render_template('index.html', data=data, prod_number=product_number_by_company)
    # return "INDEX"


class OrderedCounter(Counter, OrderedDict):
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')
