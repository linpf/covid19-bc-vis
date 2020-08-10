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

def cases_daily_age_chart():

    l = []
    age_l = []
    report_days = set()
    with open("../data/Covid19Canada/cases.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            l.append((row_data["date_report"],row_data["age"]))
            age_l.append(row_data["age"])
            report_days.add(row_data["date_report"])

    count = Counter(l)
    age_count = Counter(age_l)

    sorted_age = sorted(age_count.keys(), key=lambda k: -age_count[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.StackedBar(height=400,show_x_labels=True,x_label_rotation=0.01, 
        show_legend=True,show_minor_x_labels=False)
    for age in sorted_age:
        cases_per_day = []
        for day in sorted_report_days:
            if (day,age) in count:
                cases_per_day.append(count[(day,age)])
            else:
                cases_per_day.append(None)
        chart.add(age, cases_per_day)
    chart.title = "Daily Cases by age"
    chart.x_labels = sorted_report_days 
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    chart.render_to_file('daily_cases_by_age_stacked_chart.svg')
if __name__ == "__main__":
    cases_daily_age_chart()
