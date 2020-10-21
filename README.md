## Black Friday App
Non-official application that determines whether the prices of discounted Black Friday products on Altex are really lower than usual.
## Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Scraper](/scraper/README.md)
- [API](/api/README.md)
- [Web App](/web_app/README.md)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## About <a name = "about"></a>
This app allows you to search for products on [Altex](https://www.altex.ro/) and extract some useful information (price, discounted price). For the moment, the app allows you to scrape multiple pages, which means that you will get multiple products. Using the API or the Web App, you can search for a specific product. \
\
On the Web App you can find some statistics about the companies, and visualize for each product, the evolution in time of the price. 

## Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
### Prerequisites
- Git
- Docker

### Installing

First of all, you have to create a local copy (a clone) of this repository on your computer. Change the current working directory to the location where you want the cloned directory and run:

```powershell
git clone https://github.com/ionescuvlad97/black-friday-app.git
```
Once you installed `docker`, `docker-compose` was also installed. Make sure that docker is running. You have to create the containers of the app, so in the working directory run:
```
docker-compose build
```

## Usage <a name="usage"></a>
Add notes about how to use the system.

## Built Using <a name = "built_using"></a>
- [SQLAlchemy](https://www.sqlalchemy.org/)/[MySQL](https://www.mysql.com/)- Database
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Web Framework
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Web Scraping
