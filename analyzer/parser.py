import csv
from constants import BANK1_HEADER_FIELDS, BANK2_HEADER_FIELDS
from utils import date_from_string


def meta_parser(filename):
    if 'statements.csv' in filename:
        return parser_bank(filename, BANK1_HEADER_FIELDS)
    else:
        return parser_bank(filename, BANK2_HEADER_FIELDS)


def parser_bank(filename, header_fields):
    result = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
                obj = {
                    'date': date_from_string(row[header_fields['date']], header_fields['date_format']),
                    'description': row[header_fields['description']].strip(),
                    'amount': header_fields['sign'] * float(row[header_fields['amount']])
                }
                result.append(obj)
    return result    
