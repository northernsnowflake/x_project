url = "https://www.sreality.cz/hledani/prodej/domy/kralovehradecky-kraj,pardubicky-kraj?region=m%C4%9Bstsk%C3%A1%20%C4%8D%C3%A1st%20B%C4%9Ble%C4%8Dko&no_shares=1&region-id=148&region-typ=ward&bez-aukce=1&vzdalenost=5#z=12"
# for testing
#url = "https://www.sreality.cz/hledani/prodej/domy/kralovehradecky-kraj,pardubicky-kraj?no_shares=1&region=B%C3%BD%C5%A1%C5%A5&region-id=2551&region-typ=municipality&bez-aukce=1&vzdalenost=5"

import sqlite3
import requests 
from bs4 import BeautifulSoup


from selenium import webdriver
from selenium.webdriver.common.by import By


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

zaznamy = []

#brave
BROWSER_PATH = r"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
OPTIONS = webdriver.ChromeOptions()
OPTIONS.binary_location = BROWSER_PATH
OPTIONS.add_experimental_option("detach", True)

# webdriver, další 2 řádky must have 
# mám odsud https://stackoverflow.com/questions/76550506/typeerror-webdriver-init-got-an-unexpected-keyword-argument-executable-p
driver=webdriver.Chrome(options=OPTIONS)
driver.get(url) 

time.sleep(3)


cookie = {
    'name': 'euconsent-v2',
    'value': 'CP6iR4AP6iR4AD3ACBCSApEsAP_gAEPgAATIJVwQQAAwAKAAsACAAFQALgAZAA6ACAAFAAKgAWgAyABoADmAIgAigBHACSAEwAJwAVQAtgBfgDCAMUAgACEgEQARQAjoBOAE6AL4AaQA4gB3ADxAH6AQgAkwBOACegFIAKyAWYAuoBgQDTgG0APkAjUBHQCaQE2gJ0AVIAtQBbgC8wGMgMkAZcA0oBqYDugHfgQHAhcBGYCVYIXQIoAFAAWABUAC4AIAAZAA0ACIAEcAJgAVQAtgBiAD8AISARABEgCOAE4AMsAZoA7gB-gEIAIsAXUA2gCbQFSALUAW4AvMBggDJAGpgQuAAAAA.YAAAAAAAAAAA',
    'path': '/',
    'domain': '.sreality.cz',  # Change this to your domain
    'secure': True  # Set True if the cookie should only be transmitted over HTTPS
}
driver.add_cookie(cookie)
driver.refresh()
#driver.get(url) 

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


def print_data(connetion):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM nabídka")
    items = cursor.fetchall()
    return items 


try:
    print(response.text)
    # část selenia, browser se musí načíst a pak refreshovat 
    time.sleep(10)

    soup.prettify()
    
    #elems = WebDriverWait(driver, 2.5).until(EC.presence_of_element_located((By.ID, "h2")))

    elements = driver.find_elements(By.CLASS_NAME, 'title')  # You can change 'a' to another tag if needed

    for element in elements:
        odkaz = element.get_attribute('href')
        if odkaz != None:
            print(odkaz)
            zaznamy.append(odkaz)
        else:
            pass

    slovnik = dict(enumerate(zaznamy))

    #create_table_nabidka(connection)
    #insert_into_nabidka(connection, slovnik)
    #for item in print_data(connection): 
    #    print(item[1])  

 
    #next_button = driver.execute_script("arguments[0].scrollIntoView(true)")
    #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.scmp-btn--default[data-testid='button-agree']"))).click()
    #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='scmp-btn scmp-btn--default' and @data-testid='button-agree']"))).click()
    #/html/body/div[3]//div/div/div[2]/button[2]/span
    #/html/body/div[3]//div/div/div[2]/button[2]
    
    # Click the "Consent with Personalization" button
    ######WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.scmp-btn--default[data-testid='button-agree']"))).click()
    #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.scmp-btn--default[data-testid='button-agree']"))).click()


    #https://python-forum.io/thread-9525.html
    ######arrow = driver.find_elements(By.CLASS_NAME, 'paging-next')[0]
    #arrow = driver.find_elements(By.CLASS_NAME, 'btn-paging-on icof icon-arr-right paging-next')[0]
    #arrow = driver.find_elements_by_xpath('//*[@id="page-layout"]/div[2]/div[3]/div[3]/div/div/div/div/div[3]/div/div[26]/ul[2]/li[6]/a')[0]
   
    #while arrow != 'disabled':
    #    arrow.click()
    
    #####arrow.click()
    time.sleep(5)

    elements = driver.find_elements(By.CLASS_NAME, 'title') 
    
    for element in elements:
        odkaz = element.get_attribute('href')
        if odkaz != None:
            print(odkaz)
            zaznamy.append(odkaz)
        else:
            pass
           
    #element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'btn-paging-on icof icon-arr-right paging-next'))
    #WebDriverWait(driver, 2.5).until(element_present)
    #except TimeoutException:
    #print("Timed out waiting for page to load")
#except NoSuchElementException:
    #print("Button not found or not visible.")
finally:
    # commitnout náš příkaz a zavřít connection
    connection.commit()
    connection.close()
    driver.quit()
    #print('Page loaded')


#<button type="button" class="scmp-btn scmp-btn--default" data-testid="button-agree">  <span class="">Souhlasím</span></button>
# 
# X Path /html/body/div[3]//div/div/div[2]/button[2]
#
#



