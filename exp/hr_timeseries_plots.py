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

def prov_hrs_mortality_bar_chart(province):

    with open("../data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        data_x_y = {} 
        hrs_list = {} 
        hrs_cumulative = {} 
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_death_report"],row_data["health_region"])] = int(row_data["deaths"])
                hrs_list[row_data["health_region"]] = int(row_data["deaths"]) 
                hrs_cumulative[row_data["health_region"]] = int(row_data["cumulative_deaths"]) 

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_hrs = sorted(hrs_list.keys(), key=lambda k: -hrs_cumulative[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.StackedBar(height=360,show_x_labels=False,legend_at_bottom=True)
    for hr in sorted_hrs:
        series_data_list = []
        for day in sorted_report_days:
            if (day,hr) in data_x_y:
                series_data_list.append(data_x_y[(day,hr)])
            else:
                series_data_list.append(None)
        chart.add(hr, series_data_list)
    chart.title = province + " COVID-19 deaths per Health Region"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('death_by_hrs_line_chart.svg')

def prov_hrs_cases_bar_chart(province):

    with open("../data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        data_x_y = {} 
        hrs_list = {} 
        hrs_cumulative = {} 
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_report"],row_data["health_region"])] = int(row_data["cases"])
                hrs_list[row_data["health_region"]] = int(row_data["cases"]) 
                hrs_cumulative[row_data["health_region"]] = int(row_data["cumulative_cases"]) 

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_hrs = sorted(hrs_list.keys(), key=lambda k: -hrs_cumulative[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.StackedBar(height=360,show_x_labels=False,legend_at_bottom=True)
    for hr in sorted_hrs:
        series_data_list = []
        for day in sorted_report_days:
            if (day,hr) in data_x_y:
                series_data_list.append(data_x_y[(day,hr)])
            else:
                series_data_list.append(None)
        chart.add(hr, series_data_list)
    chart.title = province + " cases per Health Region"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('cases_by_hrs_line_chart.svg')

def prov_hrs_mortality_cumulative_line_chart(province):

    with open("../data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        data_x_y = {} 
        hrs_list = {} 
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_death_report"],row_data["health_region"])] = int(row_data["cumulative_deaths"])
                hrs_list[row_data["health_region"]] = int(row_data["cumulative_deaths"]) 

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_hrs = sorted(hrs_list.keys(), key=lambda k: -hrs_list[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.Line(height=360,show_x_labels=False,legend_at_bottom=True)
    for hr in sorted_hrs:
        series_data_list = []
        for day in sorted_report_days:
            if (day,hr) in data_x_y:
                series_data_list.append(data_x_y[(day,hr)])
            else:
                series_data_list.append(None)
        chart.add(hr, series_data_list)
    chart.title = f"cumulative deaths by {province} HRs"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('cumulative_death_by_hrs_line_chart.svg')

def prov_hrs_cumulative_cases_line_chart(province):

    with open("../data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        data_x_y = {} 
        hrs_list = {} 
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_report"],row_data["health_region"])] = int(row_data["cumulative_cases"])
                hrs_list[row_data["health_region"]] = int(row_data["cumulative_cases"]) 

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_hrs = sorted(hrs_list.keys(), key=lambda k: -hrs_list[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.Line(height=360,show_x_labels=False,legend_at_bottom=True)
    for hr in sorted_hrs:
        series_data_list = []
        for day in sorted_report_days:
            if (day,hr) in data_x_y:
                series_data_list.append(data_x_y[(day,hr)])
            else:
                series_data_list.append(None)
        chart.add(hr, series_data_list)
    chart.title = "cumulative cases by HRs"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('cumulative_cases_by_hrs_line_chart.svg')

if __name__ == "__main__":
    prov_hrs_cumulative_cases_line_chart("BC")
    prov_hrs_mortality_cumulative_line_chart("BC")
    prov_hrs_cases_bar_chart("BC")
    prov_hrs_mortality_bar_chart("BC")
