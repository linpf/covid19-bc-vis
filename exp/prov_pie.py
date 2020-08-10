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
    provs_latest_report_date = {}

    with open("../data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            provs_data[(row_data["province"])] = int(row_data["cumulative_cases"])
            provs_latest_report_date[(row_data["province"])] = row_data["date_report"]
            province = row_data["province"] 

    sorted_provs = sorted(prov_hrs.keys(),key=lambda province : -provs_data[province])) 

    chart = pygal.Pie(height=400)

    for province in sorted_provs:
        prov_provs_data = []
        for hr in prov_hrs[province]:
            prov_provs_data.append({'value' : provs_data[(province,hr)], 'label' : hr})
        chart.add(province,sorted(prov_provs_data,key=lambda hr: -hr["value"]))
    chart.title =  "Latest cumulative cases updated on " + str(set(provs_latest_report_date.values())) + " per Health Region"
    chart.render_to_file('health_regions_cumulative_cases_chart.svg')

def provs_cases_pie_chart():

    provs_data = {} 
    provs_latest_report_date = {}
    prov_hrs = {}

    with open("../data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            provs_data[(row_data["province"],row_data["health_region"])] = int(row_data["cases"])
            provs_latest_report_date[(row_data["province"],row_data["health_region"])] = row_data["date_report"]
            province = row_data["province"] 
            if province not in prov_hrs:
                prov_hrs[province] = set()
            else:
                prov_hrs[province].add(row_data["health_region"])

    sorted_provs = sorted(prov_hrs.keys(),key=lambda province : -sum([
        provs_data[province,hr] for hr in prov_hrs[province]])) 

    chart = pygal.Pie(height=400)

    for province in sorted_provs:
        prov_provs_data = []
        for hr in prov_hrs[province]:
            prov_provs_data.append({'value' : provs_data[(province,hr)], 'label' : hr})
        chart.add(province,sorted(prov_provs_data,key=lambda hr: -hr["value"]))
    chart.title =  "Latest new cases on " + str(set(provs_latest_report_date.values())) + " per Health Region"
    chart.render_to_file('health_regions_sorted_by_prov_chart.svg')

def prov_provs_cumulative_cases_lines_chart(province,health_region):

    provs_data = {} 
    groups_list = {} 

    with open("../data/Covid19Canada/timeseries_prov/mortality_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                provs_data[(row_data["date_death_report"],"cumulative_deaths")] = int(row_data["cumulative_deaths"])
                groups_list["cumulative_deaths"] = int(row_data["cumulative_deaths"]) 

    with open("../data/Covid19Canada/timeseries_prov/cases_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                provs_data[(row_data["date_report"],"cumulative_cases")] = int(row_data["cumulative_cases"])
                groups_list["cumulative_cases"] = int(row_data["cumulative_cases"]) 

    report_days = set()
    for key in provs_data:
        day = key[0]
        report_days.add(day)
    
    sorted_groups = sorted(groups_list.keys(), key=lambda k: -groups_list[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.Line(height=400,show_x_labels=False,legend_at_bottom=True)
    for group in sorted_groups:
        cumulative_data_list = []
        for day in sorted_report_days:
            if (day,group) in provs_data:
                cumulative_data_list.append(provs_data[(day,group)])
            else:
                cumulative_data_list.append(None)
        chart.add(group, cumulative_data_list)
    
    chart.title = health_region + " (" + province + ") cumulative cases data"
    chart.x_labels = sorted_report_days 
    chart.render_to_file(province+"_"+health_region+'_cumulative_data_lines_chart.svg')

if __name__ == "__main__":
#    prov_provs_cumulative_cases_lines_chart("BC","Fraser")
    provs_cases_pie_chart()
    provs_cases_pie_chart2()
    provs_cumulative_cases_pie_chart()
