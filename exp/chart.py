import pygal
import csv
from collections import Counter
l = []
with open("../data/Covid19Canada/cases.csv", 'r') as file:
    csv_file = csv.DictReader(file)
    for row in csv_file:
        row_data = dict(row)
        l.append(row_data["province"])
count = Counter(l)
print(count)
for key in count:
    print(key,count[key])

print("keys",count.keys())
print("values",count.values())
    
chart = pygal.Bar()
chart.title = "Case # by Province"
sorted_key = sorted(count.keys(),key=lambda key: -count[key])
print("sorted_keys",sorted_key)
for key in sorted_key:
    chart.add(key,[count[key]])
chart.render()
chart.render_to_file('bar_chart.svg')
