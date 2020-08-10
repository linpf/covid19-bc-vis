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

#==> cases_timeseries_prov.csv <==
#"province","health_region","date_report","cases","cumulative_cases"
#"Alberta","Calgary","25-01-2020",0,0
#"Alberta","Calgary","26-01-2020",0,0
#"Alberta","Calgary","27-01-2020",0,0
#"Alberta","Calgary","28-01-2020",0,0
#"Alberta","Calgary","29-01-2020",0,0
#"Alberta","Calgary","30-01-2020",0,0
#"Alberta","Calgary","31-01-2020",0,0
#"Alberta","Calgary","01-02-2020",0,0
#"Alberta","Calgary","02-02-2020",0,0
#
#==> mortality_timeseries_prov.csv <==
#"province","health_region","date_death_report","deaths","cumulative_deaths"
#"Alberta","Calgary","08-03-2020",0,0
#"Alberta","Calgary","09-03-2020",0,0
#"Alberta","Calgary","10-03-2020",0,0
#"Alberta","Calgary","11-03-2020",0,0
#"Alberta","Calgary","12-03-2020",0,0
#"Alberta","Calgary","13-03-2020",0,0
#"Alberta","Calgary","14-03-2020",0,0
#"Alberta","Calgary","15-03-2020",0,0
#"Alberta","Calgary","16-03-2020",0,0

def provs_cumulative_cases_pie_chart():

    provs_data = {} 
    groups_list = {} 
    provs_latest_report_date = {}

    with open("../data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            province = row_data["province"]
            provs_data[province] = int(row_data["cumulative_cases"])
            provs_latest_report_date[province] = row_data["date_report"]

    chart = pygal.Pie(height=400)

    sorted_provs = sorted(provs_data.keys(),key=lambda province: -provs_data[province])
    for province in sorted_provs:
        if provs_data[province] != 0:
            chart.add(province,[provs_data[province]])
    chart.title =  "cumulative cases on per Province"
    chart.render_to_file('provs_cumulative__cases_pie_chart.svg')

def provs_cumulative_cases_bar_chart():

    provs_data = {} 
    groups_list = {} 
    provs_latest_report_date = {}

    with open("../data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            province = row_data["province"]
            provs_data[province] = int(row_data["cumulative_cases"])
            provs_latest_report_date[province] = row_data["date_report"]

    chart = pygal.Bar(height=320)

    sorted_provs = sorted(provs_data.keys(),key=lambda province: -provs_data[province])
    for province in sorted_provs:
        chart.add(province,[provs_data[province]])
    chart.title =  "cumulative cases per Province"
    chart.render_to_file('provs_cumulative_cases_bar_chart.svg')

def provs_mortality_cumulative_bar_chart():

    provs_data = {} 
    groups_list = {} 
    provs_latest_report_date = {}

    with open("../data/Covid19Canada/timeseries_prov/mortality_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            province = row_data["province"]
            provs_data[province] = int(row_data["cumulative_deaths"])
            provs_latest_report_date[province] = row_data["date_death_report"]

    chart = pygal.Bar(height=320)

    sorted_provs = sorted(provs_data.keys(),key=lambda province: -provs_data[province])
    for province in sorted_provs:
        chart.add(province,[provs_data[province]])
    chart.title =  "cumulative mortality per Province"
    chart.render_to_file('provs_mortality_cumulative_bar_chart.svg')

def provs_new_cases_bar_chart():

    provs_data = {} 
    provs_latest_report_date = {}

    with open("../data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            province = row_data["province"]
            provs_data[province] = int(row_data["cases"])
            provs_latest_report_date[province] = row_data["date_report"]

    chart = pygal.Bar(height=400)

    sorted_provs = sorted(provs_data.keys(),key=lambda province: -provs_data[province])
    sorted_provs = [ prov for prov in sorted_provs if provs_data[prov] != 0]
    print(provs_data)
    print(sorted_provs)
    for province in sorted_provs:
        chart.add(province,[provs_data[province]])
    chart.title =  "Latest new cases on " + str(set(provs_latest_report_date.values())) + " per Province"
    chart.render_to_file('provs_new_cases_bar_chart.svg')

if __name__ == "__main__":
#    provs_new_cases_bar_chart()
#    provs_cumulative_cases_pie_chart()
    provs_mortality_cumulative_bar_chart()
    provs_cumulative_cases_bar_chart()
