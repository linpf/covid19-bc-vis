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

def cases_daily_travel_history_country_chart():

    l = []
    country_l = []
    report_days = set()
    with open("../data/Covid19Canada/cases.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            l.append((row_data["date_report"],row_data["travel_history_country"]))
            country_l.append(row_data["travel_history_country"])
            report_days.add(row_data["date_report"])

    count = Counter(l)
    country_count = Counter(country_l)

    sorted_country = sorted(country_count.keys(), key=lambda k: -country_count[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.StackedBar(width=1800,height=900,show_x_labels=True,x_label_rotation=0.01, show_legend=True,show_minor_x_labels=False)
    for country in sorted_country:
        cases_per_day = []
        for day in sorted_report_days:
            if (day,country) in count:
                cases_per_day.append(count[(day,country)])
            else:
                cases_per_day.append(None)
        chart.add(country, cases_per_day)
    chart.title = "Cases with travel_history_country"
    chart.x_labels = sorted_report_days 
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    chart.render_to_file('cases_with_travel_history_country_stacked_chart.svg')
if __name__ == "__main__":
    cases_daily_travel_history_country_chart()
