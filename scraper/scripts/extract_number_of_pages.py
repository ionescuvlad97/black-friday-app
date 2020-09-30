from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
test_url = 'https://altex.ro/telefoane-samsung/cpl/'
altex_test_page = urlopen(test_url)
altex_test_soup = bs(altex_test_page, 'html.parser')

main_container = altex_test_soup.find('div', {'class': 'lg-u-float-right lg-u-size-8of10'})
sort_container = main_container.find('div', {'class': 'u-container-reset u-border-t-solid'})
select_page_container = sort_container.find('div', {'class': 'u-display-iblock Toolbar-pager'})
pages_url = select_page_container.findAll('option')
url_list = []
for elem in pages_url:
    url_list.append(elem['value'])
print(url_list)