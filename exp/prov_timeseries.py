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

with open("../data/Covid19Canada/timeseries_prov/mortality_timeseries_prov.csv", 'r') as file:
    data_x_y = {} 
    provinces_list = {} 
    csv_file = csv.DictReader(file)
    for row in csv_file:
        row_data = dict(row)
        data_x_y[(row_data["date_death_report"],row_data["province"])] = int(row_data["deaths"])
        provinces_list[row_data["province"]] = int(row_data["cumulative_deaths"]) 

    report_day_set = set()
    for key in data_x_y:
        day = key[0]
        report_day_set.add(day)

    print(provinces_list)
    sorted_provinces = sorted(provinces_list.keys(), key=lambda k: -provinces_list[k])
    sorted_report_days = sorted(list(report_day_set),key=day_month_year)
    print("sorted provinces",sorted_provinces)
    print("sorted report_days",sorted_report_days)
    chart = pygal.StackedBar(width=1200,height=600,show_legend=True)
    for province in sorted_provinces:
        province_cases_per_day = []
        for day in sorted_report_days:
            if (day,province) in data_x_y:
                province_cases_per_day.append(data_x_y[(day,province)])
            else:
                province_cases_per_day.append(None)
        chart.add(province, province_cases_per_day)
    chart.title = "daily death cases # by province"
    chart.x_labels = sorted_report_days 
    chart.render_to_file('deaths_x_y_bar_chart.svg')
