import pygal
import csv
import sys
from collections import Counter
import datetime 

def day_month_year(date):
    l = date.split("-")
    ## year:month:day
    return l[2] + l[1] + l[0]

def display_year_month_day(date):
    l = date.split("-")
    return l[2] + "-" + l[1] + "-" + l[0]

#==> cases_timeseries_prov.csv <==
#"province","date_report","cases","cumulative_cases"
#"Alberta","25-01-2020",0,0
#"Alberta","26-01-2020",0,0
#"Alberta","27-01-2020",0,0
#"Alberta","28-01-2020",0,0
#"Alberta","29-01-2020",0,0
#"Alberta","30-01-2020",0,0
#"Alberta","31-01-2020",0,0
#"Alberta","01-02-2020",0,0
#"Alberta","02-02-2020",0,0

def provs_testing_stacked_bar_chart():

    d1 = datetime.date.today()
    with open("../data/Covid19Canada/timeseries_prov/testing_timeseries_prov.csv", 'r') as file:
        data_x_y = {} 
        provinces_list = {} 
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_testing"],row_data["province"])] = int(row_data["testing"])
            provinces_list[row_data["province"]] = int(
            row_data["cumulative_testing"]) 

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    ### trying to align testing x-axis with cases x-axis

    with open("../data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            report_days.add(row_data["date_report"])

    sorted_provinces = sorted(provinces_list.keys(), key=lambda k: -provinces_list[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.StackedBar(height=320,show_x_labels=False)
    for province in sorted_provinces:
        province_cases_per_day = []
        for day in sorted_report_days:
            if (day,province) in data_x_y:
                province_cases_per_day.append(data_x_y[(day,province)])
            else:
                province_cases_per_day.append(None)
        chart.add(province, province_cases_per_day)
    chart.title = "daily testing by province"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('provs_testing_stackedbar_chart.svg')

def provs_cases_stacked_bar_chart():
    d1 = datetime.date.today()
    with open("../data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        data_x_y = {} 
        provinces_list = {} 
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_report"],row_data["province"])] = int(row_data["cases"])
            provinces_list[row_data["province"]] = int( row_data["cumulative_cases"]) 

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_provinces = sorted(provinces_list.keys(), key=lambda k: -provinces_list[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.StackedBar(height=320,show_x_labels=False)
    for province in sorted_provinces:
        province_cases_per_day = []
        for day in sorted_report_days:
            if (day,province) in data_x_y:
                province_cases_per_day.append(data_x_y[(day,province)])
            else:
                province_cases_per_day.append(None)
        chart.add(province, province_cases_per_day)
    chart.title = "daily cases by province"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('provs_cases_stackedbar_chart.svg')

if __name__ == "__main__":
    provs_cases_stacked_bar_chart()
    provs_testing_stacked_bar_chart()
