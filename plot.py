"""
Plot localities using Google Maps
"""
import random

from tqdm import tqdm
from jinja2 import Template
import yaml

from models import connect_db


db = connect_db()
table = db['papeletas']

data = table.all()
data = [
    i
    for i in data
    if i['latitude'] is not None and i['longitude'] < -77.070554
]
points = [
    "new google.maps.LatLng({}, {}),".format(
        i['latitude'], i['longitude']
    )
    for i in random.sample(data, 500)
]

with open("config.yml", "r") as handle:
    GOOGLE_MAPS_API_KEY = yaml.load(handle.read())['GOOGLE_MAPS_API_KEY']

with open("template.html", "r") as handle:
    html = handle.read()

# new google.maps.LatLng(37.782551, -122.445368),
template = Template(html)
x = template.render(
    google_maps_api_key=GOOGLE_MAPS_API_KEY,
    points="\n".join(points),
)
print(x)
