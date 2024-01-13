url = "https://www.sreality.cz/hledani/prodej/domy/kralovehradecky-kraj,pardubicky-kraj?region=m%C4%9Bstsk%C3%A1%20%C4%8D%C3%A1st%20B%C4%9Ble%C4%8Dko&no_shares=1&region-id=148&region-typ=ward&bez-aukce=1&vzdalenost=5#z=12"

import sqlite3
import requests 
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
import time

zaznamy = []

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
# přidáme nové jméno databáze, musí končit '.db' 
connection = sqlite3.connect("domy.db", timeout = 60)

# je to objekt, přes který se zadávají sql příkazy
# vytvoříme instanci cursor
#cursor = connection.cursor()

def create_table_nabidka(connection):
    cursor = connection.cursor()
    query = """CREATE TABLE nabídka
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            odkaz TEXT NOT NULL
        );
        """
    '''
    query = """CREATE TABLE nabídka
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            odkaz TEXT NOT NULL,
            nazev TEXT,
            vzdalenost TEXT,
            cena NUMERIC
        );
        """
    '''
    cursor.execute(query) # vytvoření tabulky

def insert_into_nabidka(connection, slovnik):
    cursor = connection.cursor()
    data = [(url_add,) for url_add in slovnik.values()] 
    cursor.executemany("INSERT INTO nabídka (odkaz) VALUES (?)", data)
    '''
    query = """
        INSERT INTO nabídka (odkaz, nazev, vzdalenost, cena)
        VALUES ('odkaz', 'Belecko3', '0.2km', '4000000')
        """
    '''
    #return cursor.execute(query) # insert into tabulka

#print('Command executed successfully...')

try:
    print(response.text)

    # část selenia, browser se musí načíst a pak refreshovat 
    time.sleep(2.5)
    #driver.refresh() # odebrala jsem, je zbytečné

    soup.prettify()
    
    #elems = WebDriverWait(driver, 2.5).until(EC.presence_of_element_located((By.ID, "h2")))

    #hledá všechny 'a'
    #links = soup.find_all('a')  

    #for link in links:
        #print(link.get('href'))
    
    #elements = elems.find_elements(By.TAG_NAME, 'a')
    #elements = driver.find_elements(By.TAG_NAME, 'a')  # You can change 'a' to another tag if needed
    elements = driver.find_elements(By.CLASS_NAME, 'title')  # You can change 'a' to another tag if needed

    for element in elements:
        odkaz = element.get_attribute('href')
        if odkaz != None:
            print(odkaz)
            zaznamy.append(odkaz)
        else:
            pass
    #print(zaznamy)

    slovnik = dict(enumerate(zaznamy))

    insert_into_nabidka(connection, slovnik)


    
finally:
    # commitnout náš příkaz a zavřít connection
    connection.commit()
    connection.close()
    driver.quit()
