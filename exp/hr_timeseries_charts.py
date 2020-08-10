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

#==> cases_timeseries_hr.csv <==
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
#==> mortality_timeseries_hr.csv <==
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

def hr_cases_bar_chart(province,health_region):

    data_x_y = {} 
    groups_list = {} 

    with open("../data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y[(row_data["date_report"],"cases")] = int(row_data["cases"])
                groups_list["cases"] = int(row_data["cases"]) 

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)
    
    sorted_groups = sorted(groups_list.keys(), key=lambda k: -groups_list[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.Bar(height=400,show_x_labels=False,legend_at_bottom=True)
    for group in sorted_groups:
        data_list = []
        for day in sorted_report_days:
            if (day,group) in data_x_y:
                data_list.append(data_x_y[(day,group)])
            else:
                data_list.append(None)
        chart.add(group, data_list)
    
    chart.title = health_region + " (" + province + ") daily cases"
    chart.x_labels = sorted_report_days 
    chart.render_to_file(province + "_" + health_region + '_cases_bar_chart.svg')

def hr_cumulative_cases_lines_chart(province,health_region):

    data_x_y = {} 
    groups_list = {} 

    with open("../data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y[(row_data["date_death_report"],"cumulative_deaths")] = int(row_data["cumulative_deaths"])
                groups_list["cumulative_deaths"] = int(row_data["cumulative_deaths"]) 

    with open("../data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                data_x_y[(row_data["date_report"],"cumulative_cases")] = int(row_data["cumulative_cases"])
                groups_list["cumulative_cases"] = int(row_data["cumulative_cases"]) 

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)
    
    sorted_groups = sorted(groups_list.keys(), key=lambda k: -groups_list[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.Line(height=400,show_x_labels=False,legend_at_bottom=True)
    for group in sorted_groups:
        cumulative_data_list = []
        for day in sorted_report_days:
            if (day,group) in data_x_y:
                cumulative_data_list.append(data_x_y[(day,group)])
            else:
                cumulative_data_list.append(None)
        chart.add(group, cumulative_data_list)
    
    chart.title = health_region + " (" + province + ") cumulative cases data"
    chart.x_labels = sorted_report_days 
    chart.render_to_file(province+"_"+health_region+'_cumulative_data_lines_chart.svg')

if __name__ == "__main__":
    hr_cumulative_cases_lines_chart("BC","Fraser")
    hr_cases_bar_chart("BC","Fraser")
