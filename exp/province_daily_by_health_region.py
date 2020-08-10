import pygal
import csv
import sys
from collections import Counter

def day_month_year(date):
    l = date.split("-")
    ## year:month:day
    return l[2] + l[1] + l[0]

def display_month_day(date):
    l = date.split("-")
    return l[1] + "-" + l[0]

with open("../data/Covid19Canada/cases.csv", 'r') as file:
    l = []
    hr_l = []
    csv_file = csv.DictReader(file)
    for row in csv_file:
        row_data = dict(row)
        if row_data["province"] == sys.argv[1]:
            l.append((row_data["date_report"],row_data["health_region"]))
            hr_l.append(row_data["health_region"])

    count = Counter(l)
    hr_count = Counter(hr_l)

    day_set = set()
    for key in count:
        day = key[0]
        day_set.add(day)

    sorted_health_region = sorted(hr_count.keys(), key=lambda k: -hr_count[k])
    sorted_day = sorted(list(day_set),key=day_month_year)
    chart = pygal.StackedBar(width=1800,height=900,show_legend=True,x_label_rotation=60)
    for health_region in sorted_health_region:
        cases_per_day = []
        for day in sorted_day:
            if (day,health_region) in count:
                cases_per_day.append(count[(day,health_region)])
            else:
                cases_per_day.append(None)
        chart.add(health_region, cases_per_day)
    chart.title = sys.argv[1]+" daily cases # by health region"
    chart.x_labels = sorted_day 
    chart.render_to_file(sys.argv[1]+'_by_health_region_and_day_stack_chart.svg')
