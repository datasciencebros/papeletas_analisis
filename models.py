import os

import dataset
import sqlalchemy


DB_FILE = "papeletas.sqlite"


def connect_db():
    if not os.path.isfile(DB_FILE):
        db = dataset.connect(
            "sqlite:///{}".format(DB_FILE),
        )
        table = db.create_table('papeletas')
        table.create_column("dni", sqlalchemy.String)
        table.create_column("fecha_infraccion", sqlalchemy.Date)
        table.create_column("lugar_infraccion", sqlalchemy.String)
        table.create_column("papeleta", sqlalchemy.String)
        table.create_column("placa", sqlalchemy.String)

        table.create_column("deuda", sqlalchemy.Float)
        table.create_column("infraccion", sqlalchemy.String)
        table.create_column("infractor", sqlalchemy.String)
        table.create_column("propietario", sqlalchemy.String)

        table.create_index([
            'dni',
            'fecha_infraccion',
            'lugar_infraccion',
            'papeleta',
            'placa',
        ])
    else:
        db = dataset.connect(
            "sqlite:///{}".format(DB_FILE),
        )
    return db
