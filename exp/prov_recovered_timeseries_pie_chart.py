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

with open("../data/Covid19Canada/timeseries_prov/recovered_timeseries_prov.csv", 'r') as file:
    provinces_recovered = {} 
    csv_file = csv.DictReader(file)
    for row in csv_file:
        row_data = dict(row)
        provinces_recovered[row_data["province"]] = int(row_data["cumulative_recovered"]) 

    sorted_provinces = sorted(provinces_recovered.keys(), key=lambda k: -provinces_recovered[k])
    chart = pygal.Pie(height=400)
    for k in sorted_provinces:
        chart.add(k, [provinces_recovered[k]])
    chart.title = "cumulative recovered by province"
    chart.render_to_file('prov_cumulative_recovered_pie_chart.svg')
