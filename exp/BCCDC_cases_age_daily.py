import pygal
import csv
from collections import Counter

#"Reported_Date","HA","Sex","Age_Group","Classification_Reported"
#"2020-01-26","Out of Canada","M","40-49","Lab-diagnosed"
#"2020-02-02","Vancouver Coastal","F","50-59","Lab-diagnosed"
#"2020-02-05","Out of Canada","F","20-29","Lab-diagnosed"
#"2020-02-05","Out of Canada","M","30-39","Lab-diagnosed"
#"2020-02-11","Interior","F","30-39","Lab-diagnosed"
#"2020-02-20","Fraser","F","30-39","Lab-diagnosed"
#"2020-02-21","Fraser","M","40-49","Lab-diagnosed"
#"2020-02-27","Vancouver Coastal","F","60-69","Lab-diagnosed"
#"2020-02-28","Vancouver Coastal","F","30-39","Lab-diagnosed"

def day_month_year(date):
    l = date.split("-")
    ## year:month:day
    return l[2] + l[1] + l[0]

def display_month_day(date):
    l = date.split("-")
    return l[1] + "-" + l[0]

def bccdc_cases_daily_age_chart():

    l = []
    age_l = []
    report_days = set()
    with open("../data/BCCDC_COVID19_Dashboard_Case_Details.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            l.append((row_data["Reported_Date"],row_data["Age_Group"]))
            age_l.append(row_data["Age_Group"])
            report_days.add(row_data["Reported_Date"])

    count = Counter(l)
    age_count = Counter(age_l)

    #sorted_age = sorted(age_count.keys(), key=lambda k: -age_count[k])
    sorted_age = sorted(age_count.keys())
    sorted_report_days = sorted(report_days)
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
    chart.title = "Daily Cases by age group"
    chart.x_labels = sorted_report_days 
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    chart.render_to_file('bccdc_daily_cases_by_age_stacked_chart.svg')

    chart = pygal.Bar(height=400,show_x_labels=True, show_legend=True)
    for age in sorted_age:
        chart.add(age, [ age_count[age] ])
    chart.title = "BC reported Cases by age"
    chart.x_labels = ["age"]
    chart.render_to_file('bccdc_cases_by_age_stacked_chart.svg')

if __name__ == "__main__":
    bccdc_cases_daily_age_chart()
