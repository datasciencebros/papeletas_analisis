"""
Update our database with cleaned and normalized localities from file
"""
import sys
from tqdm import tqdm

from models import connect_db


filename = sys.argv[1].strip()

with open(filename, "r") as handle:
    data = handle.readlines()

db = connect_db()
table = db['papeletas']

for line in tqdm(data):
    line = line.strip().split("\t")
    try:
        locality = line[1]
    except IndexError:
        locality = ""
    data = dict(papeleta=line[0], lugar_infraccion=locality)
    table.update(data, ['papeleta'])
