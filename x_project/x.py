URL = "https://www.sreality.cz/hledani/prodej/domy/kralovehradecky-kraj,pardubicky-kraj?region=m%C4%9Bstsk%C3%A1%20%C4%8D%C3%A1st%20B%C4%9Ble%C4%8Dko&no_shares=1&region-id=148&region-typ=ward&bez-aukce=1&vzdalenost=10#z=12"

import sqlite3

# vytvoří soubor domy.db pokud neexistuje
connection = sqlite3.connect("domy.db", timeout = 60)

# je to objekt, přes který se zadávají sql příkazy
cursor = connection.cursor()



query = """CREATE TABLE nabídka
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nazev TEXT NOT NULL,
        vzdalenost TEXT NOT NULL,
        cena TEXT NOT NULL

    );
    """

try:
    cursor.execute(query).fetchall() 
finally:
    connection.commit()
    connection.close()
