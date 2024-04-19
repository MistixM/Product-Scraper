'''
    Script that will scap local shop and put all data to the SQLite database.
    Database don't use any protection
'''

import requests
import sqlite3 # SQLite database
import time

from bs4 import BeautifulSoup # For scraping

def main():
    db = sqlite3.connect('products.db') # Connect to exists database
    c = db.cursor() # Create cursor

    create_sqltable(c) # Create a database table

    # Start scraping with delays using start_scraping() function
    start_scraping(c, db, 4, 'https://linella.md/ru/catalog/fruktyi_i_ovoschi')

    print("Scraping has been finished.. Waiting for the next..")
    time.sleep(5)
    
    start_scraping(c, db, 2, 'https://linella.md/ru/catalog/moloko')
    
    print("Scraping has been finished.. Waiting for the next..")
    time.sleep(5)
    
    start_scraping(c, db, 2, 'https://linella.md/ru/catalog/kefir')
    
    print("Scraping has been finished.. Waiting for the next..")
    time.sleep(5)
    
    start_scraping(c, db, 4, 'https://linella.md/ru/catalog/yogurtyi')
    
    print("Scraping has been finished.. Waiting for the next..")
    time.sleep(5)
    
    start_scraping(c, db, 2, 'https://linella.md/ru/catalog/smetana')
    
    print("Scraping has been finished.. Waiting for the next..")
    time.sleep(5)
    
    start_scraping(c, db, 2, 'https://linella.md/ru/catalog/tvorog_svejiy')
    
    print("Scraping has been finished.. Waiting for the next..")
    time.sleep(5)
    
    start_scraping(c, db, 2, 'https://linella.md/ru/catalog/drugie_svejie_produktyi')
    
    print("Scraping has been finished.. Waiting for the next..")
    time.sleep(5)
    
    start_scraping(c, db, 2, 'https://linella.md/ru/catalog/slivki_i_sguschennoe_moloko')
    
    print("Scraping has been finished.. Waiting for the next..")
    time.sleep(5)
    
    start_scraping(c, db, 2, 'https://linella.md/ru/catalog/desertyi')
    
    print("Scraping has been finished.. Waiting for the next..")
    time.sleep(5)
    
    start_scraping(c, db, 2, 'https://linella.md/ru/catalog/maslo_i_margarin')

    # And finally tell to user scraper status
    print("Finished!")

'''
    The function go through the website and start scrap all needed data (name, price, id and link)
    Required parameters:
    -> c - database cursor
    -> db - database itself
    -> count - how many pages user want to scrap
    -> url - required url
'''
def start_scraping(c, db, count, url):
    pcount = 0 # Just for debugging

    # Start the loop for scrap each website page
    for num in range(1, count):
        content = requests.get(url + f'?page={num}') # Using concatenation plus required element to the URL adress

        soup = BeautifulSoup(content.text, 'html.parser') # Add the content to the soup

        products = soup.find_all('div', class_='products-catalog-content__body') # Then, get HTML tag that will contain all important data in one place

        # Check each tag product
        for product in products:
            # Here, just try to get all data below (name, price, id and link)
            try:
                name = product.find('a', class_='products-catalog-content__name')
                price = product.find('span', class_='price-products-catalog-content__static')

                # Just save link to product
                details_content = requests.get(f"https://linella.md{name['href']}")

                # And open this link using new soup
                detail_soup = BeautifulSoup(details_content.text, 'html.parser')
                
                # It's required to get product ID
                card = detail_soup.find('div', 'rht__block_2')
                id = card.find('span')

                # When all data has been received without any errors. Execute to database and commit changes
                c.execute("INSERT INTO data VALUES(?, ?, ?, ?)", (name.text, price.contents[0].text.strip(), id.text, f"https://linella.md{name['href']}"))
                db.commit()

            # This error is caused by tag. Scraper can't get "default price", because current price is new for product
            except AttributeError:
                # When the product have a new price (offer) just find this new tag
                new_price = product.find('span', class_='price-products-catalog-content__new')
                
                # And again try, sometimes product can't be found and it will cause error
                try:
                    # If everything is correct - execute and commit changes to the database
                    c.execute("INSERT INTO data VALUES(?, ?, ?, ?)", (name.text, new_price.contents[0].text.strip(), id.text, f"https://linella.md{name['href']}"))
                    db.commit()

                # So if product doesn't exists in the shop, just skip because we don't need it
                except Exception as e:
                    print(f"{e} Error..")
                    pass

            # Just for debug            
            pcount += 1
            print(pcount)

# Create a new table if its exist, otherwise it will send the explanation message
def create_sqltable(cursor):
    if not table_exists(cursor, "data"):
        cursor.execute("""
        CREATE TABLE data(
            name text,
            price integer,
            id integer,
            link text
        )
        """)
    else:
        print("Table already exists")

# Function that will check if table exists using sqlite_master
def table_exists(cursor, table_name):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cursor.fetchone() is not None


if __name__ == "__main__":
    main()