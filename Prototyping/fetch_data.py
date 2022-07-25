from unittest.util import strclass
import urllib.request
import json
import time
import sqlite3

KEY = open("key.txt").read()
DATABASE_PATH = "prices.sqlite"
TABLE_NAME = "prices"

def db_connection(path: str):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except sqlite3.Error as e:
        print("Error:", e)
    return connection

# get the current EUR price of a cryptocurrency by inputing the sticker symbol
def current_price(id: str) -> tuple():
    url = "https://api.nomics.com/v1/currencies/ticker?key=" + KEY + "&ids="+ id +"&interval=1d,30d&convert=EUR&platform-currency=ETH&per-page=100&page=1"
    json_file = urllib.request.urlopen(url)
    json_dict = json.load(json_file)[0]
    return (json_dict['price'], json_dict["price_timestamp"])

def get_prices_constantly(id1: str):
    start = time.time()
    print("price", " "*7, "timestamp")
    while True:
        connection = db_connection(DATABASE_PATH)
        cur = connection.cursor()
        price, timestamp = current_price(id1)
        year = int(timestamp[:4])
        months = int(timestamp[5:7])
        days = int(timestamp[8:10])
        hours = int(timestamp[11:13])
        minutes = int(timestamp[14:16])

        minutes_since_2022 = minutes + 60*hours + 24*60*days + 30*24*60*months + 12*30*24*60*(year-2022)

        print(price, minutes_since_2022)
        try:
            cur.execute(f"INSERT INTO prices VALUES ('{id1}', {price}, {minutes_since_2022})")
        except:
            print("failed to insert into database", price, minutes_since_2022)
        connection.commit()

        time.sleep(60.0 - ((time.time() - start) % 60.0))


get_prices_constantly("ETH")