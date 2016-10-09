# -*- coding: utf-8 -*-
from datetime import datetime


def strip_symbols(value):
    return value.replace(",", "").replace("-", "").replace(".", "").replace("_", "")


def clean_item(item):
    if item['infractor'] == ". .":
        item['infractor'] = ""
    if item['placa'] == ".":
        item['placa'] = ""
    if item['fecha_infraccion']:
        item['fecha_infraccion'] = datetime.strptime(
            item['fecha_infraccion'],
            '%Y-%m-%d',
        ).date()
    if item['deuda']:
        item['deuda'] = float(item['deuda'].replace(",", ""))

    if item['dni'] == "SDNI":
        item['dni'] = ""
    elif item['dni'] == "S/N":
        item['dni'] = ""
    else:
        item['dni'] = strip_symbols(item['dni'])

    if item['propietario'] == ".":
        item['propietario'] = ""
    elif item['propietario'] == ". .":
        item['propietario'] = ""
    elif item['propietario'] == "- .":
        item['propietario'] = ""

    if item['brevete']:
        item['brevete'] = strip_symbols(item['brevete'])

    for k, v in item.items():
        if type(v) == str:
            item[k] = v.replace("�", "ñ")
    return item
