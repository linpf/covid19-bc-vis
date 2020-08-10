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

#==> testing_timeseries_prov.csv <==
#"province","date_testing","testing","cumulative_testing","testing_info"
#"Alberta","15-03-2020",7108,7108,""
#"Alberta","16-03-2020",3490,10598,""
#"Alberta","17-03-2020",1757,12355,""
#"Alberta","18-03-2020",2211,14566,""
#"Alberta","19-03-2020",2447,17013,""
#"Alberta","20-03-2020",3347,20360,""
#"Alberta","21-03-2020",3382,23742,""
#"Alberta","22-03-2020",3257,26999,""
#"Alberta","23-03-2020",3059,30058,""

def provs_cases_compared_line_chart():

    with open("../data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        data_x_y = {} 
        provinces_list = {} 
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_report"],row_data["province"])] = int(row_data["cumulative_cases"])
            provinces_list[row_data["province"]] = int(row_data["cumulative_cases"]) 

    days_report = set()
    for key in data_x_y:
        day = key[0]
        days_report.add(day)

    sorted_provinces = sorted(provinces_list.keys(), key=lambda k: -provinces_list[k])
    sorted_report_days = sorted(list(days_report),key=day_month_year)
    chart = pygal.Line(height=360,show_x_labels=False,legend_at_bottom=True)
    for province in sorted_provinces:
        province_cases_per_day = []
        for day in sorted_report_days:
            if (day,province) in data_x_y:
                province_cases_per_day.append(data_x_y[(day,province)])
            else:
                province_cases_per_day.append(None)
        chart.add(province, province_cases_per_day)
    chart.title = "cumulative cases by province"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('cumulative_cases_by_province_line_chart.svg')

def provs_testing_compared_line_chart():

    with open("../data/Covid19Canada/timeseries_prov/testing_timeseries_prov.csv", 'r') as file:
        data_x_y = {} 
        provinces_list = {} 
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_testing"],row_data["province"])] = int(
                row_data["cumulative_testing"])
            provinces_list[row_data["province"]] = int(
                row_data["cumulative_testing"]) 

    days_report = set()
    for key in data_x_y:
        day = key[0]
        days_report.add(day)

    sorted_provinces = sorted(provinces_list.keys(), key=lambda k: -provinces_list[k])
    sorted_report_days = sorted(list(days_report),key=day_month_year)
    chart = pygal.Line(height=360,show_x_labels=False,legend_at_bottom=True)
    for province in sorted_provinces:
        province_cases_per_day = []
        for day in sorted_report_days:
            if (day,province) in data_x_y:
                province_cases_per_day.append(data_x_y[(day,province)])
            else:
                province_cases_per_day.append(None)
        chart.add(province, province_cases_per_day)
    chart.title = "cumulative testing by province"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('cumulative_testing_x_y_line_chart.svg')

if __name__ == "__main__":
    provs_testing_compared_line_chart()
    provs_cases_compared_line_chart()
