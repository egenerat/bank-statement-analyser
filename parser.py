import csv
import sys
import datetime
from constants import BANK1_HEADER_FIELDS, BANK2_HEADER_FIELDS, CATEGORIES, DIRECT_DEBIT_PAYMENT


def format_amount(amount):
    print "{:10.2f}".format(amount)
    
def format_column(text):
    return "{:10.2f}".format(text)


def date_from_string(str_date, pattern):
    return datetime.datetime.strptime(str_date, pattern).date()


def order_by_category(expenses, categories):
    result = {}
    # initiate result
    for i in categories:
        result[i] = {
            'amount': 0,
            'obj': []
        }

    for i in expenses:
        is_categorized = False
        for j in categories:
            for k in categories[j]:
                if k.lower() in i['description'].lower():
                    result[j]['amount'] += i['amount']
                    result[j]['obj'].append(i)
                    is_categorized = True
        if not is_categorized:
            result['unCategorized']['amount'] += i['amount']
            result['unCategorized']['obj'].append(i)
    return result


def get_filename():
    return sys.argv[1:]


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


def sum_total_expenses(data_dict):
    expenses_sum = 0
    transaction_nb = 0
    for i in data_dict:
        if DIRECT_DEBIT_PAYMENT.lower() not in i['description'].lower():
            expenses_sum += i['amount']
            transaction_nb += 1
    return {
        'expenses_sum': expenses_sum,
        'transaction_nb': transaction_nb
    }


def display_highest_amounts(expenses):
    sorted_result = sorted(expenses, key=lambda x: x['amount'], reverse=True)
    for i in sorted_result:
        print('{date} {description} {amount}'.format(date=i['date'], description=i['description'], amount=i['amount']))


def display_sorted_categories(expenses):
    result_to_display = order_by_category(expenses, CATEGORIES)
    sorted_result = sorted(result_to_display.items(), key=lambda x: x[1], reverse=True)

    for i in sorted_result:
        category_amount = i[1]['amount']
        if category_amount > 0:
            print('{cat}: {amount}'.format(cat=i[0], amount=category_amount))
    
    if result_to_display['unCategorized']['amount'] <> 0:
        print('unCategorized:')
        print(result_to_display['unCategorized'])
        for i in result_to_display['unCategorized']['obj']:
            print(i)

if __name__ == '__main__':
    filename_list = get_filename()
    expenses = []
    for filename in filename_list:
        expenses += meta_parser(filename)

    print(expenses)

    display_highest_amounts(expenses)
    print(sum_total_expenses(expenses))

    display_sorted_categories(expenses)
