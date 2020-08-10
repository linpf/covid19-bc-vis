import pygal
import csv
from collections import Counter

def day_month_year(date):
    l = date.split("-")
    ## year:month:day
    return l[2] + l[1] + l[0]

def display_month_day(date):
    l = date.split("-")
    return l[1] + "-" + l[0]

def prov_hrs_cases_bar_chart(province):
    with open("../data/Covid19Canada/cases.csv", 'r') as file:
        l = []
        hr_l = []
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                l.append((row_data["date_report"],row_data["health_region"]))
                hr_l.append(row_data["health_region"])

    count = Counter(l)
    hr_count = Counter(hr_l)

    report_days = set()
    for key in count:
        day = key[0]
        report_days.add(day)

    sorted_day = sorted(list(report_days),key=day_month_year)
    chart = pygal.StackedBar(width=1800,height=900,show_legend=True,x_label_rotation=60)
    sorted_hr = sorted(hr_count.keys(),key = lambda hr : -sum([count[(d,h)] for(d,h) in count if h == hr]))
    for hr in sorted_hr:
        cases_per_day = []
        for day in sorted_day:
            if (day,hr) in count:
                cases_per_day.append(count[(day,hr)])
            else:
                cases_per_day.append(None)
        chart.add(hr, cases_per_day)
    chart.title = ""
    chart.x_labels = sorted_day 
    chart.render_to_file('prov_trs_chart1.svg')

def prov_hrs_cases_bar_chart2(province):

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

    daily_sum = {}
    for key in data_x_y:
        day = key[0]
        hr = key[1]
        if day not in daily_sum:
            daily_sum[day] = 0
        daily_sum[day] += data_x_y[(day,hr)] 

    report_days = [d for d in daily_sum if daily_sum[d] != 0]
    sorted_hrs = sorted(hrs_list.keys(), key=lambda k: -hrs_cumulative[k])
    sorted_report_days = sorted(list(report_days),key=day_month_year)
    chart = pygal.StackedBar(width=1800,height=900,show_legend=True,x_label_rotation=60)
#    chart = pygal.StackedBar(height=360,show_x_labels=False,legend_at_bottom=True)
    for hr in sorted_hrs:
        series_data_list = []
        for day in sorted_report_days:
            if (day,hr) in data_x_y:
                series_data_list.append(data_x_y[(day,hr)])
            else:
                series_data_list.append(None)
        chart.add(hr, series_data_list)
    chart.title = ""
    chart.x_labels = sorted_report_days 
    chart.render_to_file('prov_trs_chart2.svg')

if __name__ == "__main__":
    prov_hrs_cases_bar_chart("BC")
    prov_hrs_cases_bar_chart2("BC")
