# -*- coding: utf-8 -*-
"""
Some coordinates seem to be wrong (outside El Callao). Inspect, fix or delete
"""
import argparse
import json

from models import connect_db
from utils import clean_item


def filter_items(args):
    db = connect_db()
    table = db['papeletas']
    res = table.all()
    for item in res:
        if item['latitude'] is not None:
            should_be_done = (
                item['latitude'] < float(args.latitude) and
                item['longitude'] > float(args.longitude)
            )
            if should_be_done:
                print(item)



def get_papeletas(table):
    return [i['papeleta'] for i in table.all()]


def main():
    parser = argparse.ArgumentParser(description="Inspect coordinates")
    parser.add_argument(
        '-lat',
        '--latitude',
        dest='latitude',
        action='store',
        help='Minimum latitude to use as boundary',
        required=True,
    )
    parser.add_argument(
        '-long',
        '--longitude',
        dest='longitude',
        action='store',
        help='Minimum longitude to use as boundary',
        required=True,
    )
    args = parser.parse_args()
    filter_items(args)


if __name__ == "__main__":
    main()
