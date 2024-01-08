url = "https://www.sreality.cz/hledani/prodej/domy/kralovehradecky-kraj,pardubicky-kraj?region=m%C4%9Bstsk%C3%A1%20%C4%8D%C3%A1st%20B%C4%9Ble%C4%8Dko&no_shares=1&region-id=148&region-typ=ward&bez-aukce=1&vzdalenost=5#z=12"

import sqlite3
import requests 
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
import time


#brave
BROWSER_PATH = r"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
OPTIONS = webdriver.ChromeOptions()
OPTIONS.binary_location = BROWSER_PATH
OPTIONS.add_experimental_option("detach", True)

driver=webdriver.Chrome(options=OPTIONS)

# webdriver, další 2 řádky must have 
# mám odsud https://stackoverflow.com/questions/76550506/typeerror-webdriver-init-got-an-unexpected-keyword-argument-executable-p
# tohle přidat - driver=webdriver.Chrome()
driver.get(url) 

# uložení objektu do proměnné response
response = requests.get(url)

# rozparsovat response content
soup = BeautifulSoup(response.text, "html.parser")

# vytvoří soubor domy.db pokud neexistuje
connection = sqlite3.connect("domy.db", timeout = 60)

# je to objekt, přes který se zadávají sql příkazy
cursor = connection.cursor()

query = """CREATE TABLE nabídka
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nazev TEXT NOT NULL,
        vzdalenost TEXT NOT NULL,
        cena NUMERIC NOT NULL

    );
    """
try:
    #cursor.execute(query)
    print(response.text)

    # část selenia, browser se musí načíst a pak refreshovat 
    time.sleep(3)
    driver.refresh()

    soup.prettify()
    
    #hledá všechny 'a'
    #links = soup.find_all('a')  

    #for link in links:
        #print(link.get('href'))
    
    elements = driver.find_elements(By.TAG_NAME, 'a')  # You can change 'a' to another tag if needed

    for element in elements:
        odkaz = element.get_attribute('href')
        print(odkaz)

    
finally:
    connection.commit()
    connection.close()
