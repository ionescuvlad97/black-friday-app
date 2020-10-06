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

product_tags = [
    ("div", {"class": "Product-list-right"}),
    ('h2', {'class': 'Product-nameHeading'}),
    ('div', {'class': 'Price'}),
    ('div', {'class': 'Price-current'}),
    ('span', {'class': 'Price-int'}),
    ('sup', {'class': 'Price-dec'}),
    ('div', {'class': 'Price-old'})
]


def find_altex_sub_pages(page_url):
    """Find all the sub pages of a section from altex.ro

    Because this site has a maximum limit of products that can be
    displayed (48 products per page), in one category may be multiple
    pages. This function returns URLs for all this pages.

    Args:
        param1 (str): The url of the main category

    Returns:
        list: A list that contains the URLs of the subpages
    """

    # The path to the container which contains the subpages URLs
    path = [
        ('div', {'class': 'lg-u-float-right lg-u-size-8of10'}),
        ('div', {'class': 'u-container-reset u-border-t-solid'}),
        ('div', {'class': 'u-display-iblock Toolbar-pager'})
    ]

    soup = bs(urlopen(page_url), 'html.parser')
    for div in path:
        soup = soup.find(*div)

    return [page['value'] for page in soup.findAll('option')]


def altex_etl_data(page_url):
    """Extract, Transform and Load data from altex.ro

    Apply ETL to one category of products from altex site.
    Phase 1: extract data form the category URL.
    Phase 2: transform data to fit the database
    Phase 3: load data to testdb database

    Args:
        param1 (str): The url of the category

    Returns:
        None
    """
    for page in find_altex_sub_pages(page_url):
        soup = bs(urlopen(page), 'html.parser')
        product_list = soup.findAll(*product_tags[0])

        for product in product_list:
            # Phase 1 - Extract

            name_container = product.find(*product_tags[1])
            price_container = product.find(*product_tags[2])
            current_price_container = price_container.find(*product_tags[3])
            current_price_int = current_price_container.find(*product_tags[4])
            current_price_dec = current_price_container.find(*product_tags[5])
            old_price_container = price_container.find(*product_tags[6])

            # Phase 2 - Transform

            description = name_container.a['title'].split(',')

            # The flag represent the extra number of words of the product
            # type like 'Laptop Gaming', 'Televizor Smart Curbat'
            # except the basic product types like 'Televizor' or 'Laptop'
            flag_laptop = 0
            flag_tv = 0
            old_price = 0

            # If laptop_flag is 1 means that the laptop is for gaming
            # and all indices will be shifted with 1 position
            if 'Gaming' in description[0].split() \
                        and description[0].split()[0] == 'Laptop':
                flag_laptop = 1
            if description[0].split()[0] == 'Televizor':
                flag_tv += 1
                if 'Smart' in description[0].split():
                    flag_tv += 1
                if 'Curbat' in description[0].split():
                    flag_tv += 1

            product_type = ' '.join(description[0].split()[0:1
                                                           + flag_laptop
                                                           + flag_tv])
            product_comp = description[0].split()[1 + flag_laptop + flag_tv]
            product_name = ' '.join(description[0].split()[2
                                                           + flag_laptop
                                                           + flag_tv:])
            product_specifications = ', '.join(description[1:])
            current_price = float(''.join(current_price_int.get_text() \
                                                           .split('.'))
                                    + '.'
                                    + current_price_dec.get_text()[1])
            if old_price_container is not None:
                old_price = float(''.join(old_price_container.get_text()  \
                                                             .split('.')) \
                                    .replace(',', '.'))

            # Phase 3 - Load

            session = Session()

            if (product_type,) not in session.query(ProductType.name).all():
                session.add(ProductType(product_type))
            type_id = session.query(ProductType.id) \
                             .filter(ProductType.name == product_type) \
                             .first()[0]

            if (product_comp,) not in session.query(Company.name).all():
                session.add(Company(product_comp))
            company_id = session.query(Company.id) \
                                .filter(Company.name == product_comp) \
                                .first()[0]

            if (product_name, product_specifications) \
                not in session.query(Product.name,
                                     Product.specifications) \
                              .all():
                session.add(Product(
                                product_name,
                                product_specifications,
                                type_id,
                                company_id))
            product_id = session.query(Product.id) \
                                .filter(Product.name == product_name) \
                                .filter(Product.specifications
                                        == product_specifications) \
                                .first()[0]

            price_insert = Price(product_id, current_price, old_price)

            session.add(price_insert)
            session.commit()

            session.close()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    url_lst = [line.strip() for line in open("./scripts/altex_urls.txt", "r")]
    for url in url_lst:
        altex_etl_data(url)
