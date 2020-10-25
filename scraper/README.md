# Scraper

**Status:** Working

For the moment, this scraper is works only for Altex website. Because every website has its unique structure, there is no universal solution for web scraping (maybe just for now, who knows what things AI can do in the future). You can use this scraper as a starting point for extracting data from other websites. In orther to do that, you need to understand the website’s structure. 

**Note:** Always use the `check_permission()` function. 

## Start scraping data

Run in main directory:
```
docker-compose up -d
```
Go to scripts folder:
```
cd scraper/scripts
```
Now you have to add the URLs of the products cateogories whose data you want to extract in `altex_urls.txt`. By default there will be three URLs:
```
https://altex.ro/iphones/cpl/
https://altex.ro/telefoane-samsung/cpl/
https://altex.ro/telefoane-huawei/cpl/
```	
After all the services are started and up to date, run:
```
docker-compose exec python_app python ./scripts/bf_scraper.py
````
