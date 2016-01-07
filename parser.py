import csv
import sys
import datetime

CATEGORIES = {
    'groceries': ['tesco'],
    'groceries_plus': ['SAINSBURYS', 'MARKS & SPENCER', 'M&S', 'waitrose'],
    'work_restaurant': ['UPAY'],
    'restaurant': ['paul', 'chez antoinette', 'ELECTRIC CINEMA', 'BENS COOKIES', 'MCDONALDS',
    'TINSELTOWN', 'SANTA MARIA'],
    'bars': ['BAVARIAN VILLAGE', 'UNDERBELLY LIMITED'], 
    'club': ['TIGER TIGER'],
    'clothes': ['primark'],
    'transport': ['GWR', 'LUL TICKET'],
    'phone': ['giffgaff'],
    'miscallenous': ['CARDS GALORE'],
    'repayments': ['DIRECT DEBIT PAYMENT'],
    'unCategorized': []
}


def date_from_string(str_date):
    return datetime.datetime.strptime(str_date, "%d/%m/%Y").date()


def order_by_category(expenses, categories):
    result = {}
    # initiate result
    for i in categories:
        result[i] = {
            'amount': 0,
            'obj': []
        }
        uncategorized_description = {
            'amount': 0,
            'obj': []
        }

    for i in expenses:
        is_categorized = False
        for j in categories:
            for k in categories[j]:
                if k.lower() in i['description'].lower():
                    result[j]['amount'] += i['amount']
                    result[j]['obj'].append(i['description'])
                    is_categorized = True
        if not is_categorized:
            uncategorized_description['amount'] += i['amount']
            uncategorized_description['obj'].append(i['description'])
    return {
        'result': result,
        'uncategorized_description': uncategorized_description
    }


def get_filename():
    return sys.argv[1]


def parse_bank1(filename):
    result = []
    is_header = True
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not is_header:
                obj = {
                    # could be row[1], depends if we want the date of purchase (better),
                    # or effective date on bank account (less subject to problem 
                    # if the 2 dates are in different months)
                    'date': date_from_string(row[0]),
                    'description': row[3],
                    'amount': float(row[4])
                }
                result.append(obj)
            is_header = False
    return result


def sum_total_expenses(data_dict):
    expenses_sum = 0
    for i in data_dict:
        expenses_sum += data_dict[i]
    return expenses_sum


def display_highest_amounts(expenses):
    sorted_result = sorted(expenses, key=lambda x: x['amount'], reverse=True)
    for i in sorted_result:
        print('{date} {description} {amount}'.format(date=i['date'], description=i['description'], amount=i['amount']))


def display_sorted_categories(expenses):
    sorted_data = order_by_category(expenses, CATEGORIES)
    result_to_display = sorted_data['result']
    un_categorized = sorted_data['uncategorized_description']

    print('Results:')
    print(result_to_display)

    sorted_result = sorted(result_to_display.items(), key=lambda x: x[1], reverse=True)

    for i in sorted_result:
        print('{cat}: {amount}'.format(cat=i[0], amount=i[1]))

    print(sum_total_expenses(result_to_display))

    print('Uncategorized:')
    print(un_categorized)

if __name__ == '__main__':
    filename = get_filename()
    expenses = parse_bank1(filename)

    display_highest_amounts(expenses)
    display_sorted_categories(expenses)
