import urllib.request
import json
import time

KEY = open("key.txt").read()

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
        price, timestamp = current_price(id1)
        year = int(timestamp[:4])
        months = int(timestamp[5:7])
        days = int(timestamp[8:10])
        hours = int(timestamp[11:13])
        minutes = int(timestamp[14:16])

        minutes_since_2022 = minutes + 60*hours + 24*60*days + 30*24*60*months + 12*30*24*60*(year-2022)

        print(price, minutes_since_2022)
        time.sleep(60.0 - ((time.time() - start) % 60.0))

get_prices_constantly("ETH")