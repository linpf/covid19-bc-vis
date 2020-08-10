import pygal
import csv
from collections import Counter
l = []

def day_month_year(date):
    l = date.split("-")
    ## year:month:day
    return l[2] + l[1] + l[0]

def display_month_day(date):
    l = date.split("-")
    return l[1] + "-" + l[0]

with open("../data/Covid19Canada/cases.csv", 'r') as file:
    csv_file = csv.DictReader(file)
    for row in csv_file:
        row_data = dict(row)
        l.append(row_data["date_report"])

count = Counter(l)
chart = pygal.Bar(width=1800,height=900,show_legend=False,x_label_rotation=60)
chart.title = "Canada Case # by date"
sorted_key = sorted(count.keys(),key=day_month_year)
chart.x_labels = [ display_month_day(k) for k in sorted_key ] 
chart.add("cases number per day", [count[k] for k in sorted_key])
chart.render_to_file('day_count_report_chart.svg')
