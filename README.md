
## Black Friday App
Non-official application that determines whether the prices of discounted Black Friday products on Altex are really lower than usual. Disclaimer: Developed for educational purposes only.
## Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Scraper](/scraper/README.md)
- [Database](/dbmodels/README.md)
- [API](/api/README.md)
- [Web App](/web_app/README.md)
- [Built Using](#built_using)

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
After the repository is copied, you have to create a folder for your local database:
```
mkdir my-datavolume
```
>The name of the folder must be `my-datavolume`. If you want to use another name, you have to change the `docker-compose.yml` file. In order to do that, in docker-compose file go to `services -> mysql_db`. Look for `volumes` and change `./my-datavolume:/var/lib/mysql` to `./another-name:/var/lib/mysql`.

Once you installed `docker`, `docker-compose` was also installed. Make sure that docker is running. You have to create the containers of the app, so in the working directory run:
```
docker-compose build
```

## Usage <a name="usage"></a>

The application consists of four microservices:
- Scraper
- Database
- REST API
- Web App

First you have to start the containers in the background and leave them running:
```
docker-compose up -d
```
After all the services are running and up to date, you can start scraping data using:
```
docker-compose exec python_app python ./scripts/bf_scraper.py
```
>For more info read [Scraper](/scraper/README.md)

To see the scraped data you have three options:

 1. Directly in [Database](/dbmodels/README.md)
 2. In browser using the [API](/api/README.md)
 3. In browser using the [Web App](/web_app/README.md)

For each of these options you have to open a new console in the working directory.
### 
## Built Using <a name = "built_using"></a>
- [SQLAlchemy](https://www.sqlalchemy.org/)/[MySQL](https://www.mysql.com/)- Database
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Web Framework
- [Bootstrap](https://getbootstrap.com/) - Front-end
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Web Scraping
