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

def canada_testing_bar_chart():

    data_x_y = {} 
    groups_list = {} 
    with open("../data/Covid19Canada/timeseries_canada/testing_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_testing"],"testing")] = int(row_data["testing"])
            groups_list["testing"] = int(row_data["testing"]) 

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)
    
    sorted_groups = sorted(groups_list.keys(), key=lambda k: -groups_list[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.Line(height=400,show_x_labels=False,show_legend=False)
    for group in sorted_groups:
        data_list = []
        for day in sorted_report_days:
            if (day,group) in data_x_y:
                data_list.append(data_x_y[(day,group)])
            else:
                data_list.append(None)
        chart.add("",data_list)
    
    chart.title = "Canada daily testing"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('canada_daily_testing_bar_chart.svg')

def canada_cumulative_testing_line_chart():

    data_x_y = {} 
    groups_list = {} 
    with open("../data/Covid19Canada/timeseries_canada/testing_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_testing"],"cumulative_testing")] = int(row_data["cumulative_testing"])
            groups_list["cumulative_testing"] = int(row_data["cumulative_testing"]) 

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)
    
    sorted_groups = sorted(groups_list.keys(), key=lambda k: -groups_list[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.Line(height=400,show_x_labels=False,show_legend=False)
    for group in sorted_groups:
        data_list = []
        for day in sorted_report_days:
            if (day,group) in data_x_y:
                data_list.append(data_x_y[(day,group)])
            else:
                data_list.append(None)
        chart.add("",data_list)
    
    chart.title = "Canada cumulative testing"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('canada_cumulative_testing_line_chart.svg')

def canada_cases_bar_chart():

    data_x_y = {} 
    groups_list = {} 

    with open("../data/Covid19Canada/timeseries_canada/cases_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_report"],"cases")] = int(row_data["cases"])
            groups_list["cases"] = int(row_data["cases"]) 

    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)
    
    sorted_groups = sorted(groups_list.keys(), key=lambda k: -groups_list[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.Bar(height=400,show_x_labels=False,show_legend=False)
    for group in sorted_groups:
        data_list = []
        for day in sorted_report_days:
            if (day,group) in data_x_y:
                data_list.append(data_x_y[(day,group)])
            else:
                data_list.append(None)
        chart.add("",data_list)
    
    chart.title = "Canada confirmed cases"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('canada_daily_cases_line_chart.svg')

def canada_cases_and_testing_bar_chart():

    data_x_y = {} 
    groups_list = {} 

    with open("../data/Covid19Canada/timeseries_canada/testing_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_testing"],"testing")] = int(row_data["testing"])
            groups_list["testing"] = int(row_data["testing"]) 

    with open("../data/Covid19Canada/timeseries_canada/cases_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
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
        cumulative_data_list = []
        for day in sorted_report_days:
            if (day,group) in data_x_y:
                cumulative_data_list.append(data_x_y[(day,group)])
            else:
                cumulative_data_list.append(None)
        chart.add(group, cumulative_data_list)
    
    chart.title = "Canada cases vs testing"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('canada_cases_and_testing_bar_chart.svg')

def canada_cumulative_cases_lines_chart():

    data_x_y = {} 
    groups_list = {} 
    with open("../data/Covid19Canada/timeseries_canada/mortality_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_death_report"],"cumulative_deaths")] = int(row_data["cumulative_deaths"])
            groups_list["cumulative_deaths"] = int(row_data["cumulative_deaths"]) 

    with open("../data/Covid19Canada/timeseries_canada/recovered_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_recovered"],"cumulative_recovered")] = int(row_data["cumulative_recovered"])
            groups_list["cumulative_recovered"] = int(row_data["cumulative_recovered"]) 

    with open("../data/Covid19Canada/timeseries_canada/cases_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_report"],"cumulative_cases")] = int(row_data["cumulative_cases"])
            groups_list["cumulative_cases"] = int(row_data["cumulative_cases"]) 

    with open("../data/Covid19Canada/timeseries_canada/active_timeseries_canada.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["date_active"],"active_cases")] = int(row_data["active_cases"])
            groups_list["active_cases"] = int(row_data["active_cases"]) 
    
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
    
    chart.title = "Canada cumulative cases data"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('canada_cumulative_data_lines_chart.svg')

if __name__ == "__main__":
    #canada_cumulative_cases_lines_chart()
    canada_cases_bar_chart()
    #canada_testing_bar_chart()
    #canada_cumulative_testing_line_chart()
    #canada_cases_and_testing_bar_chart()
