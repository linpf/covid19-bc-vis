import pygal
import csv
import sys
from collections import Counter
from datetime import date
import datetime

#d1 = date.today()
#print("week no",d1.isocalendar()[1])
#print("isocalendar",d1.isocalendar())
#d2 = date.fromisoformat("2020-06-01")
#d3 = date(2020,5,28)

def report_date_to_year_week(date):
    l = date.split("-")
    d = datetime.date(int(l[2]),int(l[1]),int(l[0]))
    cal = d.isocalendar()
    return cal[:2] 

def day_month_year(date):
    l = date.split("-")
    ## year:month:day
    return l[2] + l[1] + l[0]

def display_month_day(date):
    l = date.split("-")
    return l[1] + "-" + l[0]

#==> active_timeseries_canada.csv <==
#"province","date_active","cumulative_cases","cumulative_recovered","cumulative_deaths","active_cases","active_cases_change"
#"Canada","25-01-2020",1,0,0,1,1
#"Canada","26-01-2020",1,0,0,1,0
#"Canada","27-01-2020",2,0,0,2,1
#"Canada","28-01-2020",3,0,0,3,1
#"Canada","29-01-2020",3,0,0,3,0
#"Canada","30-01-2020",3,0,0,3,0
#"Canada","31-01-2020",4,0,0,4,1
#"Canada","01-02-2020",4,0,0,4,0
#"Canada","02-02-2020",4,0,0,4,0
#
#==> cases_timeseries_canada.csv <==
#"province","date_report","cases","cumulative_cases"
#"Canada","25-01-2020",1,1
#"Canada","26-01-2020",0,1
#"Canada","27-01-2020",1,2
#"Canada","28-01-2020",1,3
#"Canada","29-01-2020",0,3
#"Canada","30-01-2020",0,3
#"Canada","31-01-2020",1,4
#"Canada","01-02-2020",0,4
#"Canada","02-02-2020",0,4
#
#==> mortality_timeseries_canada.csv <==
#"province","date_death_report","deaths","cumulative_deaths"
#"Canada","08-03-2020",1,1
#"Canada","09-03-2020",0,1
#"Canada","10-03-2020",0,1
#"Canada","11-03-2020",1,2
#"Canada","12-03-2020",0,2
#"Canada","13-03-2020",0,2
#"Canada","14-03-2020",0,2
#"Canada","15-03-2020",0,2
#"Canada","16-03-2020",3,5
#
#==> recovered_timeseries_canada.csv <==
#"province","date_recovered","recovered","cumulative_recovered"
#"Canada","12-02-2020",1,1
#"Canada","13-02-2020",0,1
#"Canada","14-02-2020",0,1
#"Canada","15-02-2020",0,1
#"Canada","16-02-2020",0,1
#"Canada","17-02-2020",0,1
#"Canada","18-02-2020",0,1
#"Canada","19-02-2020",1,2
#"Canada","20-02-2020",1,3
#
#==> testing_timeseries_canada.csv <==
#"province","date_testing","testing","cumulative_testing","testing_info"
#"Canada","15-03-2020",25983,25983,""
#"Canada","16-03-2020",8818,34801,""
#"Canada","17-03-2020",5755,40556,""
#"Canada","18-03-2020",7111,47667,""
#"Canada","19-03-2020",7915,55582,""
#"Canada","20-03-2020",20455,76037,""
#"Canada","21-03-2020",14036,90073,""
#"Canada","22-03-2020",13867,103940,""
#"Canada","23-03-2020",8211,112151,""

def canada_cases_line_chart():

    data_x_y = {} 
    with open("../data/Covid19Canada/timeseries_canada/cases_timeseries_canada.csv", 'r') as file:
        groups_list = {} 
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_report"],row_data["province"])] = int(row_data["cases"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_report_days = sorted(list(report_days),key=day_month_year)

    chart = pygal.Line(height=400)
    for province in ["Canada"]:
        province_cases_per_day = []
        for day in sorted_report_days:
            if (day,province) in data_x_y:
                province_cases_per_day.append(data_x_y[(day,province)])
            else:
                province_cases_per_day.append(None)
        chart.add(province, province_cases_per_day)
    chart.title = "Canada cases"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('canada_cases_line_chart.svg')

def canada_cases_weekly_bar_chart():

    data_x_y = {} 
    with open("../data/Covid19Canada/timeseries_canada/cases_timeseries_canada.csv", 'r') as file:
        groups_list = {} 
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            year_week = report_date_to_year_week(row_data["date_report"])
            if (year_week,"Canada") not in data_x_y:
                data_x_y[(year_week,"Canada")] = 0
            data_x_y[(year_week,"Canada")] += int(row_data["cases"])

    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart = pygal.Bar(height=400)
    for province in ["Canada"]:
        province_cases_per_day = []
        for week in sorted_report_weeks:
            if (week,province) in data_x_y:
                province_cases_per_day.append(data_x_y[(week,province)])
            else:
                province_cases_per_day.append(None)
        chart.add(province, province_cases_per_day)
    chart.title = "Canada weekly cases count"
    chart.x_labels = sorted_report_weeks 
    chart.render_to_file('canada_weekly_cases_bar_chart.svg')

def canada_7days_average_cases_and_mortality_line_chart():

    data_x_y = {} 
    with open("../data/Covid19Canada/timeseries_canada/mortality_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_death_report"],"deaths")] = int(row_data["deaths"])

    with open("../data/Covid19Canada/timeseries_canada/cases_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_report"],"cases")] = int(row_data["cases"])

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    groups = ["cases", "deaths"]

    sorted_report_days = sorted(list(report_days),key=day_month_year)
    data_7days_average = [ [0] * len(report_days) for i in range(len(groups)) ]

    for n, group in enumerate(groups):
        for d in range(6,len(report_days)):
            data_7days_total = 0
            for i in range(d - 6, d + 1):
                data_7days_total += data_x_y.get((sorted_report_days[i],group),0)
            data_7days_average[n][d] = data_7days_total / 7.0

    chart = pygal.Bar(height=320)

    for n, group in enumerate(groups):
        chart.add(group , data_7days_average[n])

    chart.title = "Canada Cases and Deaths (7 days average)"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('canada_7days_average_line_chart.svg')

if __name__ == "__main__":
#    canada_cases_7days_average_line_chart()
#    canada_cases_line_chart()
    canada_cases_weekly_bar_chart()
