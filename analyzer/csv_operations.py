import csv

def export_csv(filename, objects):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in objects:
            csv_writer.writerow(['Spam'])

if __name__ == "__main__":
    export_csv('data/output/eggs.csv', [1])
