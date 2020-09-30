# Standard library imports
import numpy as np
import datetime as dt

# Third party imports
import matplotlib.dates as mdates
from matplotlib import pyplot as plt

# Local application imports
from dbmodels.base import engine
from dbmodels.base Base
from dbmodels.base Session
from dbmodels.product import Product
from dbmodels.price import Price

session = Session()

# select products.id, products.name, count(products.id) as nr from prices left join products on prices.product_id = products.id group by products.id having nr > 1;
# select companies.name, avg(prices.current_price) as total_price_current_day, prices.date from prices left join products on prices.product_id = products.id left join companies on products.company_id = companies.id group by companies.name, prices.date;
# select companies.name as company_name, avg(prices.current_price) as total_price_current_day, prices.date from prices left join products on prices.product_id = products.id left join companies on products.company_id = companies.id left join types on products.type_id = types.id where types.name = "Telefon" group by company_name, prices.date;
input_id = input("Enter id: ")

result = session.query(Product, Price).join(Price).filter(Product.id == input_id).all()
product_name = None
current_price = []
old_price = []
dates = []
for row in result:
    product_name = row.Product.name
    product_specifications = row.Product.specifications
    current_price.append(row.Price.current_price)
    old_price.append(row.Price.old_price)
    dates.append(row.Price.date)

fig = plt.figure()
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 8})
plt.plot(dates, current_price)

axes = plt.gca()
axes.set_ylim([0,7000])
# plt.plot(dates, np.array(old_price) - np.array(current_price))
plt.xlabel('Date')
plt.ylabel('Price (Lei)')
# plt.xticks(rotation=30)
fig.autofmt_xdate()
plt.fmt_xdata = mdates.DateFormatter('%Y-%m')
plt.title(product_name + '\n' + product_specifications)
plt.show()
fig.savefig('./plots/my_figure4.png')

session.close()
