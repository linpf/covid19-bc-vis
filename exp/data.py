import csv
l = []
with open("../data/Covid19Canada/cases.csv", 'r') as file:
    csv_file = csv.DictReader(file)
    for n, row in enumerate(csv_file):
        if n < 10:
            row_data = dict(row)
            print(row_data)
