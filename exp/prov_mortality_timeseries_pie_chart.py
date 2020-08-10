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

#==> mortality_timeseries_prov.csv <==
#"province","date_death_report","deaths","cumulative_deaths"
#"Alberta","08-03-2020",0,0
#"Alberta","09-03-2020",0,0
#"Alberta","10-03-2020",0,0
#"Alberta","11-03-2020",0,0
#"Alberta","12-03-2020",0,0
#"Alberta","13-03-2020",0,0
#"Alberta","14-03-2020",0,0
#"Alberta","15-03-2020",0,0
#"Alberta","16-03-2020",0,0

with open("../data/Covid19Canada/timeseries_prov/mortality_timeseries_prov.csv", 'r') as file:
    provinces_list = {} 
    csv_file = csv.DictReader(file)
    for row in csv_file:
        row_data = dict(row)
        provinces_list[row_data["province"]] = int(row_data["cumulative_deaths"]) 

    sorted_provinces = sorted(provinces_list.keys(), key=lambda k: -provinces_list[k])
    chart = pygal.Pie(height=400)
    for k in sorted_provinces:
        chart.add(k, [provinces_list[k]])
    chart.title = "cumulative_deaths by province"
    chart.render_to_file('cumulative_deaths_pie_chart.svg')
