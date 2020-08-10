import pygal
import csv
from collections import Counter

def day_month_year(date):
    l = date.split("-")
    ## year:month:day
    return l[2] + l[1] + l[0]

def display_month_day(date):
    l = date.split("-")
    return l[1] + "-" + l[0]

def prov_hr_cases_bar_chart(province):
    with open("../data/Covid19Canada/cases.csv", 'r') as file:
        l = []
        hr_l = []
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                l.append((row_data["date_report"],row_data["health_region"]))
                hr_l.append(row_data["health_region"])

    count = Counter(l)
    hr_count = Counter(hr_l)

    report_days = set()
    for key in count:
        day = key[0]
        report_days.add(day)

    sorted_day = sorted(list(report_days),key=day_month_year)
    chart = pygal.StackedBar(width=1800,height=900,show_legend=True,x_label_rotation=60)
    sorted_hr = sorted(hr_count.keys(),key = lambda hr : -sum([count[(d,h)] for(d,h) in count if h == hr]))
    for hr in sorted_hr:
        cases_per_day = []
        for day in sorted_day:
            if (day,hr) in count:
                cases_per_day.append(count[(day,hr)])
            else:
                cases_per_day.append(None)
        chart.add(hr, cases_per_day)
    chart.title = "BC cases # by date and health region"
    chart.x_labels = sorted_day 
    chart.render_to_file('bc_by_hr_and_day_stack_chart.svg')

if __name__ == "__main__":
    prov_hr_cases_bar_chart("BC")
