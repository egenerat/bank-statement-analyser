def export_csv():
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
    pass