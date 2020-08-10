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

#==> active_timeseries_prov.csv <==
#"province","date_active","cumulative_cases","cumulative_recovered","cumulative_deaths","active_cases","active_cases_change"
#"Alberta","25-01-2020",0,0,0,0,0
#"Alberta","26-01-2020",0,0,0,0,0
#"Alberta","27-01-2020",0,0,0,0,0
#"Alberta","28-01-2020",0,0,0,0,0
#"Alberta","29-01-2020",0,0,0,0,0
#"Alberta","30-01-2020",0,0,0,0,0
#"Alberta","31-01-2020",0,0,0,0,0
#"Alberta","01-02-2020",0,0,0,0,0
#"Alberta","02-02-2020",0,0,0,0,0
#
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
#
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
#
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
#
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

def all_provs_cumulative_cases_bars_chart():

    data_x_y = {} 
    groups_list = {} 

    with open("../data/Covid19Canada/timeseries_prov/mortality_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["province"],"cumulative_deaths")] = int(row_data["cumulative_deaths"])
            groups_list["cumulative_deaths"] = int(row_data["cumulative_deaths"]) 

    with open("../data/Covid19Canada/timeseries_prov/recovered_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["province"],"cumulative_recovered")] = int(row_data["cumulative_recovered"])
            groups_list["cumulative_recovered"] = int(row_data["cumulative_recovered"]) 

    with open("../data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["province"],"cumulative_cases")] = int(row_data["cumulative_cases"])
            groups_list["cumulative_cases"] = int(row_data["cumulative_cases"]) 

    with open("../data/Covid19Canada/timeseries_prov/active_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            data_x_y[(row_data["province"],"active_cases")] = int(row_data["active_cases"])
            groups_list["active_cases"] = int(row_data["active_cases"]) 
    
    report_provinces_set = set()
    for key in data_x_y:
        province = key[0]
        report_provinces_set.add(province)
    
    sorted_groups = [ "cumulative_cases", "cumulative_recovered", "active_cases", "cumulative_deaths" ] 
    sorted_report_provinces = sorted(report_provinces_set, key=lambda k: -data_x_y[(k,"cumulative_cases")]) 
    chart = pygal.StackedBar(height=400,show_x_labels=True,legend_at_bottom=True)
    for province in sorted_report_provinces:
        cumulative_data_list = []
        for group in sorted_groups:
            if (province,group) in data_x_y:
                cumulative_data_list.append(data_x_y[(province,group)])
            else:
                cumulative_data_list.append(None)
        chart.add(province, cumulative_data_list)
    
    chart.title = "cumulative cases data"
    chart.x_labels = sorted_groups 
    chart.render_to_file('cumulative_data_bars_chart.svg')

if __name__ == "__main__":
    all_provs_cumulative_cases_bars_chart()
