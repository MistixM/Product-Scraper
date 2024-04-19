# Product Scraper
A simple scraper that get all necessary data from local shop with using ```BeautifulSoup``` as scraper library and ```sqlite3``` for storing data in database table.

[![preview.png](https://i.postimg.cc/8zKyZgzj/preview.png)](https://postimg.cc/fVdjbFXN)
## Detailed description
Target website don't have any protection so here I use library ```request``` to get all content from this website.

The parser consists of several stages:
1. Connect to the database and create table if its does not exists.
2. Preparing and start scraping all necessary data in specific function. Such as name, price, id and link.
3. Then these data will be commited to database table.
4. Repeat all steps in above if user have another links from this website (like another products to scrap).

## Functions
```start_scraping()``` - go through the website and start scrap all needed data (name, price, id and link).

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `c` | `sqlite3.cursor` | **Required**. Your cursor here |
| `db` | `sqlite3.connection` | **Required**. SQLite database |
| `count` | `int` | **Required**. How many pages user want to scrap |
| `url` | `str` | **Required**. Required URL to scrap |

```create_sqltable()``` - Create a new table if its exist, otherwise it will send the explanation message.

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `cursor` | `sqlite3.cursor` | **Required**. Your cursor here |

```table_exists()``` - Function that will check if table exists using sqlite_master.

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `cursor` | `sqlite3.cursor` | **Required**. Your cursor here |
| `table_name` | `str` | **Required**. Name for your table |