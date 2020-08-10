import pygal
import csv
from collections import Counter
import datetime

#"Reported_Date","HA","Sex","Age_Group","Classification_Reported"
#"2020-01-26","Out of Canada","M","40-49","Lab-diagnosed"
#"2020-02-02","Vancouver Coastal","F","50-59","Lab-diagnosed"
#"2020-02-05","Out of Canada","F","20-29","Lab-diagnosed"
#"2020-02-05","Out of Canada","M","30-39","Lab-diagnosed"
#"2020-02-11","Interior","F","30-39","Lab-diagnosed"
#"2020-02-20","Fraser","F","30-39","Lab-diagnosed"
#"2020-02-21","Fraser","M","40-49","Lab-diagnosed"
#"2020-02-27","Vancouver Coastal","F","60-69","Lab-diagnosed"
#"2020-02-28","Vancouver Coastal","F","30-39","Lab-diagnosed"

def bc_report_date_to_year_week(date):
    l = date.split("-")
    d = datetime.date(int(l[0]),int(l[1]),int(l[2]))
    cal = d.isocalendar()
    return cal[:2]

def day_month_year(date):
    l = date.split("-")
    ## year:month:day
    return l[2] + l[1] + l[0]

def display_month_day(date):
    l = date.split("-")
    return l[1] + "-" + l[0]

def bccdc_cases_by_age_group_charts():

    l = []
    age_l = []
    data_x_y = {}
    age_groups_list = {}
    report_days = set()

    with open("../data/BCCDC_COVID19_Dashboard_Case_Details.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            l.append((row_data["Reported_Date"],row_data["Age_Group"]))
            age_l.append(row_data["Age_Group"])
            report_days.add(row_data["Reported_Date"])
            year_week = bc_report_date_to_year_week(row_data["Reported_Date"])
            if (year_week,row_data["Age_Group"]) not in data_x_y:
                data_x_y[(year_week,row_data["Age_Group"])] = 0
            data_x_y[(year_week,row_data["Age_Group"])] += 1 
            if row_data["Age_Group"] not in age_groups_list:
                age_groups_list[row_data["Age_Group"]] = 0 
            age_groups_list[row_data["Age_Group"]] += 1 

    sorted_age_groups = sorted(age_groups_list.keys())
    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart1 = pygal.StackedBar(height=400, show_x_labels=True, show_legend=True,
    legend_at_bottom=False, x_title="Week number")
    for age_group in sorted_age_groups:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week,age_group) in data_x_y:
                timeseries_data.append(data_x_y[(week,age_group)])
            else:
                timeseries_data.append(None)
        chart1.add({"title": age_group}, timeseries_data)
                              
    chart1.title = "BC Weekly New Cases by Age Group"
    chart1.x_labels = [ w[1] for w in sorted_report_weeks ] 
    chart1.render_to_file('bccdc_weekly_cases_by_age_group_chart1.svg')

    count = Counter(l)
    age_count = Counter(age_l)

    sorted_age = sorted(age_count.keys())
    sorted_report_days = sorted(report_days)
    chart2 = pygal.StackedBar(height=400,show_x_labels=True,x_label_rotation=0.01, 
        show_legend=True,show_minor_x_labels=False)
    for age in sorted_age:
        cases_per_day = []
        for day in sorted_report_days:
            if (day,age) in count:
                cases_per_day.append(count[(day,age)])
            else:
                cases_per_day.append(None)
        chart2.add(age, cases_per_day)
    chart2.title = "Daily Cases by age group"
    chart2.x_labels = sorted_report_days 
    chart2.x_labels_major = [day for day in sorted_report_days if day[8:] == "01" ]
    chart2.render_to_file('bccdc_daily_cases_by_age_stacked_chart2.svg')

    chart3 = pygal.Bar(height=400,show_x_labels=True, show_legend=True)
    for age in sorted_age:
        chart3.add(age, [ age_count[age] ])
    chart3.title = "BC reported Cases by age"
    chart3.x_labels = ["age"]
    chart3.render_to_file('bccdc_cases_by_age_stacked_chart3.svg')

    chart4 = pygal.Bar(height=400,show_legend=True)
    last_report_day = sorted_report_days[-1]
    for age in sorted_age:
        cases_per_day = []
        for day in [ last_report_day ]:
            if (day,age) in count:
                cases_per_day.append(count[(day,age)])
            else:
                cases_per_day.append(None)
        chart4.add(age, cases_per_day)
    chart4.title = "Last Reported Day Cases by Age Group"
    chart4.render_to_file('bccdc_last_report_day_cases_by_age_bar_chart4.svg')

def bccdc_cases_daily_age_chart():

    l = []
    age_l = []
    report_days = set()
    with open("../data/BCCDC_COVID19_Dashboard_Case_Details.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            l.append((row_data["Reported_Date"],row_data["Age_Group"]))
            age_l.append(row_data["Age_Group"])
            report_days.add(row_data["Reported_Date"])

    count = Counter(l)
    age_count = Counter(age_l)

    sorted_age = sorted(age_count.keys())
    sorted_report_days = sorted(report_days)
    chart = pygal.StackedBar(height=400,show_x_labels=True,x_label_rotation=0.01, 
        show_legend=True,show_minor_x_labels=False)
    for age in sorted_age:
        cases_per_day = []
        for day in sorted_report_days:
            if (day,age) in count:
                cases_per_day.append(count[(day,age)])
            else:
                cases_per_day.append(None)
        chart.add(age, cases_per_day)
    chart.title = "Daily Cases by age group"
    chart.x_labels = sorted_report_days 
    chart.x_labels_major = [day for day in sorted_report_days if day[8:] == "01" ]
    chart.render_to_file('bccdc_daily_cases_by_age_stacked_chart.svg')

    chart = pygal.Bar(height=400,show_x_labels=True, show_legend=True)
    for age in sorted_age:
        chart.add(age, [ age_count[age] ])
    chart.title = "BC reported Cases by age"
    chart.x_labels = ["age"]
    chart.render_to_file('bccdc_cases_by_age_stacked_chart.svg')

def bccdc_cases_by_age_group_weekly_bar_chart():

    data_x_y = {}
    age_groups_list = {}
    
    with open("../data/BCCDC_COVID19_Dashboard_Case_Details.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            year_week = bc_report_date_to_year_week(row_data["Reported_Date"])
            if (year_week,row_data["Age_Group"]) not in data_x_y:
                data_x_y[(year_week,row_data["Age_Group"])] = 0
            data_x_y[(year_week,row_data["Age_Group"])] += 1 
            if row_data["Age_Group"] not in age_groups_list:
                age_groups_list[row_data["Age_Group"]] = 0 
            age_groups_list[row_data["Age_Group"]] += 1 

    sorted_age_groups = sorted(age_groups_list.keys())
    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart = pygal.StackedBar(height=400, show_x_labels=True, show_legend=True,
    legend_at_bottom=False, x_title="Week number")
    for age_group in sorted_age_groups:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week,age_group) in data_x_y:
                timeseries_data.append(data_x_y[(week,age_group)])
            else:
                timeseries_data.append(None)
        chart.add({"title": age_group}, timeseries_data)
                              
    chart.title = "BC Weekly New Cases by Age Group"
    chart.x_labels = [ w[1] for w in sorted_report_weeks ] 

    chart.render_to_file('bccdc_cases_by_age_group_weekly_chart.svg')

def bccdc_cases_by_ha_weekly_bar_chart():

    data_x_y = {}
    hrs_list = {}
    
    with open("../data/BCCDC_COVID19_Dashboard_Case_Details.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            year_week = bc_report_date_to_year_week(row_data["Reported_Date"])
            if (year_week,row_data["HA"]) not in data_x_y:
                data_x_y[(year_week,row_data["HA"])] = 0
            data_x_y[(year_week,row_data["HA"])] += 1 
            if row_data["HA"] not in hrs_list:
                hrs_list[row_data["HA"]] = 0 
            hrs_list[row_data["HA"]] += 1 

    sorted_hrs = sorted(hrs_list.keys(), key=lambda k: -hrs_list[k])
    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart = pygal.StackedBar(height=400, show_x_labels=True, show_legend=True,
    legend_at_bottom=True, x_title="Week number")
    for hr in sorted_hrs:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week,hr) in data_x_y:
                timeseries_data.append(data_x_y[(week,hr)])
            else:
                timeseries_data.append(None)
        chart.add({"title": hr}, timeseries_data)
                              
    chart.title = "BC Weekly New Cases by health region"
    chart.x_labels = [ w[1] for w in sorted_report_weeks ] 

    chart.render_to_file('bccdc_cases_by_ha_weekly_chart.svg')

if __name__ == "__main__":
#    bccdc_cases_daily_age_chart()
#    bccdc_cases_by_ha_weekly_bar_chart()
#    bccdc_cases_by_age_group_weekly_bar_chart()
    bccdc_cases_by_age_group_charts()
