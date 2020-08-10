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

def bc_cases_daily_sex_chart():

    l = []
    sex_l = []
    report_days = set()
    with open("../data/Covid19Canada/cases.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == "BC":
                l.append((row_data["date_report"],row_data["sex"]))
                sex_l.append(row_data["sex"])
                report_days.add(row_data["date_report"])

    count = Counter(l)
    sex_count = Counter(sex_l)
    print(sex_count)
    sorted_sex = sorted(sex_count.keys(), key=lambda k: -sex_count[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.StackedBar(height=400,show_x_labels=True,x_label_rotation=0.01, 
        show_legend=True,show_minor_x_labels=False)
    for sex in sorted_sex:
        cases_per_day = []
        for day in sorted_report_days:
            if (day,sex) in count:
                cases_per_day.append(count[(day,sex)])
            else:
                cases_per_day.append(None)
        chart.add(sex, cases_per_day)
    chart.title = "BC daily reported Cases by sex"
    chart.x_labels = sorted_report_days 
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    chart.render_to_file('bc_daily_cases_by_sex_stacked_chart.svg')

    chart = pygal.Bar(height=400,show_x_labels=True, show_legend=True)
    for sex in sorted_sex:
        chart.add(sex, [ sex_count[sex] ])
    chart.title = "BC reported Cases by sex"
    chart.x_labels = ["sex"]
    chart.render_to_file('bc_cases_by_sex_stacked_chart.svg')
if __name__ == "__main__":
    bc_cases_daily_sex_chart()
