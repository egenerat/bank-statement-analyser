import csv
import sys
import datetime

CATEGORIES = {
    'groceries' : ['tesco'],
    'groceries_plus': ['SAINSBURYS', 'MARKS & SPENCER', 'M&S'],
    'work_restaurant' : ['UPAY'],
    'restaurant' : ['paul', 'chez antoinette', 'ELECTRIC CINEMA', 'BENS COOKIES', 'MCDONALDS',
    'TINSELTOWN', 'SANTA MARIA'],
    'bars': ['BAVARIAN VILLAGE', 'UNDERBELLY LIMITED'], 
    'club' : ['TIGER TIGER'],
    'clothes' : ['primark'],
    'transport' : ['GWR', 'LUL TICKET'],
    'phone': ['giffgaff'],
    'miscallenous' : ['CARDS GALORE'],
    'unCategorized': []
}

def date_from_string(str_date):
    return datetime.datetime.strptime(str_date, "%d/%m/%Y").date()

def order_by_category(expenses, categories):
    result = {}
    # initiate result
    for i in categories:
        result[i] = 0
        uncategorized_description = []

    for i in expenses:
        is_categorized = False
        for j in categories:
            for k in categories[j]:
                if k.lower() in i['description'].lower():
                    result[j] += i['price']
                    is_categorized = True
        if not is_categorized:
            result['unCategorized'] += i['price']
            uncategorized_description.append(i['description'])
    return {
        'result': result,
        'uncategorized_description': uncategorized_description
    }

def get_filename():
    return sys.argv[1]

def parse(filename):
    result = []
    is_header = True
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if not is_header:
                obj = {
                    # could be row[1], depends if we want the date of purchase (better),
                    # or effective date on bank account (less subject to problem 
                    # if the 2 dates are in different months)
                    'date':date_from_string(row[0]),
                    'description':row[3],
                    'price':float(row[4])
                }
                result.append(obj)
            is_header = False
    return result

filename = get_filename()
expenses = parse(filename)
result_to_display = order_by_category(expenses, CATEGORIES)
print(result_to_display)