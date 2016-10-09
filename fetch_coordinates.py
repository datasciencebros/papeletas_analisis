"""
Fetch coordinates using Google Maps API and save them in our database
"""
from urllib.parse import quote_plus
import requests
from time import sleep

import yaml
from tqdm import tqdm

from models import connect_db


with open("config.yml", "r") as handle:
    data = yaml.load(handle.read())

GOOGLE_MAPS_API_KEY = data['GOOGLE_MAPS_API_KEY']
GOOGLE_MAPS_API_LIMIT = 2500

# "https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}"
GOOGLE_MAPS_URL_BASE = "https://maps.googleapis.com/maps/api/geocode/json?address="


def get_distinct_addresses():
    db = connect_db()
    table = db['papeletas']
    res = table.find(latitude=None)
    return list(set(
        [
            i['lugar_infraccion']
            for i in res
        ]
    ))


addresses = get_distinct_addresses()
db = connect_db()
table = db['papeletas']
for address in tqdm(addresses[0:GOOGLE_MAPS_API_LIMIT]):
    if address:
        sleep(0.1)
        url = "{0}{1}&key={2}".format(
            GOOGLE_MAPS_URL_BASE,
            quote_plus(address),
            GOOGLE_MAPS_API_KEY
        )
        res = requests.get(url)
        data = res.json()
        if data['status'] == "OK":
            coords = data['results'][0]['geometry']['location']
            latitude = coords['lat']
            longitude = coords['lng']
            data_to_update = dict(
                lugar_infraccion=address,
                latitude=latitude,
                longitude=longitude,
            )
            table.update(data_to_update, ['lugar_infraccion'])
