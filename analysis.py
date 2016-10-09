# -*- coding: utf-8 -*-
import argparse
import json

from models import connect_db
from utils import clean_item


def upload_to_db(file_name):
    """Parse json lines file and save in database if needed."""
    with open(file_name, "r") as handle:
        data = [
            json.loads(i)
            for i in handle.readlines()
        ]
    db = connect_db()
    table = db['papeletas']
    papeletas_in_db = get_papeletas(table)

    items_to_insert = [
        i
        for i in data
        if i['papeleta'] not in papeletas_in_db
    ]

    cleaned_items = [
        clean_item(item)
        for item in items_to_insert
    ]
    table.insert_many(cleaned_items)


def get_papeletas(table):
    return [i['papeleta'] for i in table.all()]


def main():
    parser = argparse.ArgumentParser(description="Analyze fines")
    parser.add_argument(
        '-i',
        '--input',
        dest='input_file',
        action='store',
        help='JsonLines file with scraped data',
        required=True,
    )
    args = parser.parse_args()
    upload_to_db(args.input_file)


if __name__ == "__main__":
    main()
