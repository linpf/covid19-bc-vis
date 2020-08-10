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

def provs_hrs_cumulative_cases_pie_chart():

    hrs_data = {} 
    hrs_latest_report_date = {}
    prov_hrs = {}

    with open("../data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            hrs_data[(row_data["province"],row_data["health_region"])] = int(row_data["cumulative_cases"])
            hrs_latest_report_date[(row_data["province"],row_data["health_region"])] = row_data["date_report"]
            province = row_data["province"] 
            if province not in prov_hrs:
                prov_hrs[province] = set()
            else:
                prov_hrs[province].add(row_data["health_region"])

    sorted_provs = sorted(prov_hrs.keys(),key=lambda province : -sum([
        hrs_data[province,hr] for hr in prov_hrs[province]])) 

    chart = pygal.Pie(height=400)

    for province in sorted_provs:
        prov_hrs_data = []
        for hr in prov_hrs[province]:
            prov_hrs_data.append({'value' : hrs_data[(province,hr)], 'label' : hr})
        chart.add(province,sorted(prov_hrs_data,key=lambda hr: -hr["value"]))
    chart.title =  "Latest cumulative cases updated on " + str(set(hrs_latest_report_date.values())) + " per Health Region"
    chart.render_to_file('health_regions_cumulative_cases_chart.svg')

def provs_hrs_cases_pie_chart():

    hrs_data = {} 
    hrs_latest_report_date = {}
    prov_hrs = {}

    with open("../data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            hrs_data[(row_data["province"],row_data["health_region"])] = int(row_data["cases"])
            hrs_latest_report_date[(row_data["province"],row_data["health_region"])] = row_data["date_report"]
            province = row_data["province"] 
            if province not in prov_hrs:
                prov_hrs[province] = set()
            else:
                prov_hrs[province].add(row_data["health_region"])

    sorted_provs = sorted(prov_hrs.keys(),key=lambda province : -sum([
        hrs_data[province,hr] for hr in prov_hrs[province]])) 

    chart = pygal.Pie(height=400)

    for province in sorted_provs:
        prov_hrs_data = []
        for hr in prov_hrs[province]:
            prov_hrs_data.append({'value' : hrs_data[(province,hr)], 'label' : hr})
        chart.add(province,sorted(prov_hrs_data,key=lambda hr: -hr["value"]))
    chart.title =  "Latest new cases on " + str(set(hrs_latest_report_date.values())) + " per Health Region"
    chart.render_to_file('health_regions_sorted_by_prov_chart.svg')


def provs_hrs_cases_pie_chart2():

    hrs_data = {} 
    groups_list = {} 
    hrs_latest_report_date = {}

    with open("../data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            hr = row_data["province"] + '-' + row_data["health_region"]
            hrs_data[hr] = int(row_data["cases"])
            hrs_latest_report_date[hr] = row_data["date_report"]

    chart = pygal.Pie(height=400)

    sorted_hr = sorted(hrs_data.keys(),key=lambda hr: -hrs_data[hr])
    for hr in sorted_hr:
        chart.add(hr,[hrs_data[hr]])
    chart.title =  "Latest new cases on " + str(set(hrs_latest_report_date.values())) + " per Health Region"
    #chart.x_labels = sorted_hr
    chart.render_to_file('health_regions_sorted_by_hr_chart.svg')

def prov_hrs_cases_bar_chart(province):

    hrs_data = {} 
    groups_list = {} 
    hrs_latest_report_date = {}

    with open("../data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                hr = row_data["health_region"]
                hrs_data[hr] = int(row_data["cases"])
                hrs_latest_report_date[hr] = row_data["date_report"]

    chart = pygal.Bar(height=400,legend_at_bottom=True)

    sorted_hr = sorted(hrs_data.keys(),key=lambda hr: -hrs_data[hr])
    for hr in sorted_hr:
        chart.add(hr,[hrs_data[hr]])
    chart.title =  "Latest new cases on " + str(set(hrs_latest_report_date.values())) + " per Health Region"
    chart.render_to_file(province+'_hrs_cases_bar_chart.svg')

def prov_hrs_cumulative_cases_bar_chart(province):

    hrs_data = {} 
    groups_list = {} 
    hrs_latest_report_date = {}

    with open("../data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                hr = row_data["health_region"]
                hrs_data[hr] = int(row_data["cumulative_cases"])
                hrs_latest_report_date[hr] = row_data["date_report"]

    chart = pygal.Bar(height=400,legend_at_bottom=True)

    sorted_hr = sorted(hrs_data.keys(),key=lambda hr: -hrs_data[hr])
    for hr in sorted_hr:
        chart.add(hr,[hrs_data[hr]])
    chart.title =  "Latest new cases on " + str(set(hrs_latest_report_date.values())) + " per Health Region"
    chart.render_to_file(province+'_hrs_cumulative_cases_bar_chart.svg')

def prov_hrs_mortality_cumulative_bar_chart(province):

    hrs_data = {} 
    groups_list = {} 
    hrs_latest_report_date = {}

#==> mortality_timeseries_hr.csv <==
#"province","health_region","date_death_report","deaths","cumulative_deaths"
#"Alberta","Calgary","08-03-2020",0,0

    with open("../data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                hr = row_data["health_region"]
                hrs_data[hr] = int(row_data["cumulative_deaths"])
                hrs_latest_report_date[hr] = row_data["date_death_report"]

    chart = pygal.Bar(height=400,legend_at_bottom=True)

    sorted_hr = sorted(hrs_data.keys(),key=lambda hr: -hrs_data[hr])
    for hr in sorted_hr:
        chart.add(hr,[hrs_data[hr]])
    chart.title =  province + " cumulative deaths per Health Region"
    chart.render_to_file(province+'_hrs_cumulative_deaths_bar_chart.svg')

def prov_hrs_cumulative_cases_lines_chart(province,health_region):

    hrs_data = {} 
    groups_list = {} 

    with open("../data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                hrs_data[(row_data["date_death_report"],"cumulative_deaths")] = int(row_data["cumulative_deaths"])
                groups_list["cumulative_deaths"] = int(row_data["cumulative_deaths"]) 

    with open("../data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province and row_data["health_region"] == health_region:
                hrs_data[(row_data["date_report"],"cumulative_cases")] = int(row_data["cumulative_cases"])
                groups_list["cumulative_cases"] = int(row_data["cumulative_cases"]) 

    report_days = set()
    for key in hrs_data:
        day = key[0]
        report_days.add(day)
    
    sorted_groups = sorted(groups_list.keys(), key=lambda k: -groups_list[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.Line(height=400,show_x_labels=False,legend_at_bottom=True)
    for group in sorted_groups:
        cumulative_data_list = []
        for day in sorted_report_days:
            if (day,group) in hrs_data:
                cumulative_data_list.append(hrs_data[(day,group)])
            else:
                cumulative_data_list.append(None)
        chart.add(group, cumulative_data_list)
    
    chart.title = health_region + " (" + province + ") cumulative cases data"
    chart.x_labels = sorted_report_days 
    chart.render_to_file(province+"_"+health_region+'_cumulative_data_lines_chart.svg')

if __name__ == "__main__":
#    prov_hrs_cumulative_cases_lines_chart("BC","Fraser")
#    provs_hrs_cases_pie_chart()
#    provs_hrs_cases_pie_chart2()
    prov_hrs_cases_bar_chart("Ontario")
    prov_hrs_cumulative_cases_bar_chart("Ontario")
    prov_hrs_mortality_cumulative_bar_chart("BC")
#    provs_hrs_cumulative_cases_pie_chart()
