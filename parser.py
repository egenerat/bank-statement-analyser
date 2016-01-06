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

def parse_bank1(filename):
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

def sum_total_expense(data_dict):
	sum = 0
	# for i in data_dict:
	# 	sum += data_dict[i]
	return sum


if __name__ == '__main__':
	filename = get_filename()
	expenses = parse_bank1(filename)
	sorted_data = order_by_category(expenses, CATEGORIES)

	result_to_display = sorted_data['result']
	unCategorized = sorted_data['uncategorized_description']

	result_to_display = sorted(result_to_display.items(), key=lambda x:x[1], reverse=True)

	print(result_to_display)

	for i in result_to_display:
		print('{cat}: {amount}'.format(cat=i, amount=result_to_display[i]))