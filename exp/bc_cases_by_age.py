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

def bc_cases_daily_travel_history_age_chart(province):

    l = []
    age_l = []
    day_set = set()
    with open("../data/Covid19Canada/cases.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                l.append((row_data["date_report"],row_data["age"]))
                age_l.append(row_data["age"])
                day_set.add(row_data["date_report"])

    count = Counter(l)
    age_count = Counter(age_l)

    sorted_age = sorted(age_count.keys(), key=lambda k: -age_count[k])
    sorted_day = sorted(list(day_set),key=day_month_year)
    chart = pygal.StackedBar(width=1800,height=900,show_legend=True,x_label_rotation=60)
    for age in sorted_age:
        cases_per_day = []
        for day in sorted_day:
            if (day,age) in count:
                cases_per_day.append(count[(day,age)])
            else:
                cases_per_day.append(None)
        chart.add(age, cases_per_day)
    chart.title = "BC cases by age"
    chart.x_labels = sorted_day 
    chart.render_to_file('bc_cases_age_stacked_chart.svg')
if __name__ == "__main__":
    bc_cases_daily_travel_history_age_chart("BC")

