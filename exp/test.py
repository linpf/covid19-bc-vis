import pygal
import csv
import sys
import datetime
def day_month_year(date):
    l = date.split("-")
    ## year:month:day
    return l[2] + l[1] + l[0]

def display_month_day(date):
    l = date.split("-")
    return l[1] + "-" + l[0]

def prov_hrs_cases_daily_bar_chart(province):

    data_x_y = {}
    hrs_list = {}
    
    with open("../data/Covid19Canada/timeseries_hr/cases_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if row_data["province"] == province:
                data_x_y[(row_data["date_report"],row_data["health_region"])] = int(row_data["cases"])
                hrs_list[row_data["health_region"]] = int(row_data["cumulative_cases"])
                
    sorted_hrs = sorted(hrs_list.keys(),
                              key=lambda k: -hrs_list[k])
    report_days = set()
    for key in data_x_y:
        day = key[0]
        report_days.add(day)

    sorted_report_days = sorted(list(report_days), key=day_month_year)
    chart = pygal.StackedBar(height=400, show_x_labels=True, show_legend=False,
            show_minor_x_labels=False, x_label_rotation=0.01)
    for hr in sorted_hrs:
        timeseries_data = []
        for day in sorted_report_days:
            if (day,hr) in data_x_y:
                timeseries_data.append(data_x_y[(day,hr)])
            else:
                timeseries_data.append(None)
        chart.add({"title": hr}, timeseries_data)
                              
    chart.title = "{} Daily New Cases by health region".format(province)
    chart.x_labels = sorted_report_days
    chart.x_labels_major = [day for day in sorted_report_days if day[:2] == "01" ]
    chart.render_to_file('test.svg')

if __name__ == "__main__":
    prov_hrs_cases_daily_bar_chart("Ontario")
