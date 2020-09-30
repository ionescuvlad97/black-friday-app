# Standard library imports
from urllib.request import urlopen

# Third party imports
from bs4 import BeautifulSoup as bs

# Local application imports
from dbmodels.base import engine
from dbmodels.base import Base
from dbmodels.base import Session
from dbmodels.producttype import ProductType
from dbmodels.company import Company
from dbmodels.product import Product
from dbmodels.price import Price

# https://altex.ro/laptopuri/cpl/

def findAltexSubPages(page_url):
    sub_page_url_list = []
    altex_test_page = urlopen(page_url)
    altex_test_soup = bs(altex_test_page, 'html.parser')

    main_container = altex_test_soup.find('div', {'class': 'lg-u-float-right lg-u-size-8of10'})
    sort_container = main_container.find('div', {'class': 'u-container-reset u-border-t-solid'})
    select_page_container = sort_container.find('div', {'class': 'u-display-iblock Toolbar-pager'})
    pages_url = select_page_container.findAll('option')

    for elem in pages_url:
        sub_page_url_list.append(elem['value'])
    return sub_page_url_list


def extractAltexData(page_url):
    products_count = 0
    test_list = []
    # type_insert = ProductType()
    # company_insert = Company()
    # product_insert = Product()
    for page in findAltexSubPages(page_url):
        altex_samsung_page = urlopen(page)
        altex_samsung_soup = bs(altex_samsung_page, 'html.parser')
        product_list = altex_samsung_soup.findAll("div", {"class": "Product-list-right"})

        for product in product_list:
            # Name Zone
            name_container = product.find('h2', {'class': 'Product-nameHeading'})
            description = name_container.a['title'].split(',')
            # the flag represent the extra number of words of the product type except the basic product types
            # like 'Televizor' or 'Laptop'
            flag_laptop = 0
            flag_tv = 0
            if 'Gaming' in description[0].split() and description[0].split()[0] == 'Laptop':
                # if flag is 1 means that the laptop is for gaming (only for laptops) and all indices will be shifted
                # with 1 position
                flag_laptop = 1
            if description[0].split()[0] == 'Televizor':
                flag_tv += 1
                if 'Smart' in description[0].split():
                    flag_tv += 1
                if 'Curbat' in description[0].split():
                    flag_tv += 1
            product_type = ' '.join(description[0].split()[0:1 + flag_laptop + flag_tv])
            product_comp = description[0].split()[1 + flag_laptop + flag_tv]
            product_name = ' '.join(description[0].split()[2 + flag_laptop + flag_tv:])
            product_specifications = ', '.join(description[1:])

            # Price Zone
            price_container = product.find('div', {'class': 'Price'})

            # # Current Price
            current_price_container = price_container.find('div', {'class': 'Price-current'})
            current_price_int = current_price_container.find('span', {'class': 'Price-int'})
            current_price_dec = current_price_container.find('sup', {'class': 'Price-dec'})
            current_price = float(
                ''.join(current_price_int.get_text().split('.')) + '.' + current_price_dec.get_text()[1])

            # # Old Price
            old_price_container = price_container.find('div', {'class': 'Price-old'})
            old_price = 0
            if old_price_container is not None:
                old_price = float(''.join(old_price_container.get_text().split('.')).replace(',', '.'))

            print(f'Product type: {product_type}')
            print(f'Product company: {product_comp}')
            print(f'Product name: {product_name}')
            print(f'Product specifications: {product_specifications}')
            print(f'Current price: {current_price}')
            print(f'Old price: {old_price}')
            # Statistics
            print(f'Discount: {0 if old_price == 0 else old_price - current_price}')
            print(f'Discount: {0 if old_price == 0 else (old_price - current_price)*100/old_price} %')
            print()
            products_count += 1
            test_list.append(product_type)


            session = Session()

            if (product_type,) not in session.query(ProductType.name).all():
                session.add(ProductType(product_type))
            type_id = session.query(ProductType.id).filter(ProductType.name == product_type).first()[0]

            if (product_comp,) not in session.query(Company.name).all():
                session.add(Company(product_comp))
            company_id = session.query(Company.id).filter(Company.name == product_comp).first()[0]

            if (product_name, product_specifications) not in session.query(Product.name, Product.specifications).all():
                session.add(Product(
                                product_name,
                                product_specifications,
                                type_id,
                                company_id))
            product_id = session.query(Product.id).filter(Product.name == product_name).\
                                                   filter(Product.specifications == product_specifications).first()[0]

            price_insert = Price(product_id, current_price, old_price)

            session.add(price_insert)

            session.commit()

            session.close()
    # print(test_list)
    print(f'Number of products: {products_count}')


def getURLs():
    fh = open("./scripts/altex_urls.txt", "r")
    url_lst = []
    for line in fh:
        url_lst.append(line.strip())
    return url_lst


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    url_lst = getURLs()
    for url in url_lst:
        extractAltexData(url)
