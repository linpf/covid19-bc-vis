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

#==> recovered_timeseries_prov.csv <==
#"province","date_recovered","recovered","cumulative_recovered"
#"Alberta","12-02-2020",0,0
#"Alberta","13-02-2020",0,0
#"Alberta","14-02-2020",0,0
#"Alberta","15-02-2020",0,0
#"Alberta","16-02-2020",0,0
#"Alberta","17-02-2020",0,0
#"Alberta","18-02-2020",0,0
#"Alberta","19-02-2020",0,0
#"Alberta","20-02-2020",0,0

with open("../data/Covid19Canada/timeseries_prov/recovered_timeseries_prov.csv", 'r') as file:
    data_x_y = {} 
    provinces_recovered = {} 
    csv_file = csv.DictReader(file)
    for row in csv_file:
        row_data = dict(row)
        data_x_y[(row_data["date_recovered"],row_data["province"])] = int(
            row_data["cumulative_recovered"])
        provinces_recovered[row_data["province"]] = int(
            row_data["cumulative_recovered"]) 

    report_day_set = set()
    for key in data_x_y:
        day = key[0]
        report_day_set.add(day)

    sorted_provinces = sorted(provinces_recovered.keys(), key=lambda k: -provinces_recovered[k])
    sorted_report_days = sorted(list(report_day_set),key=day_month_year)
    chart = pygal.Line(height=400,show_x_labels=False,legend_at_bottom=True)
    for province in sorted_provinces:
        province_cases_per_day = []
        for day in sorted_report_days:
            if (day,province) in data_x_y:
                province_cases_per_day.append(data_x_y[(day,province)])
            else:
                province_cases_per_day.append(None)
        chart.add(province, province_cases_per_day)
    chart.title = "cumulative recovered by province"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('prov_cumulative_recovered_line_chart.svg')
