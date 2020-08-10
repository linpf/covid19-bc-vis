import pygal
import csv
from collections import Counter
import datetime

#BCCDC_COVID19_Dashboard_Lab_Information.txt
#"Date","Region","New_Tests","Total_Tests","Positivity","Turn_Around"
#2020-01-23,"BC",2,2,0,24
#2020-01-23,"Fraser",0,0,0,0
#2020-01-23,"Interior",0,0,0,0
#2020-01-23,"Northern",0,0,0,0
#2020-01-23,"Unknown",0,0,0,0
#2020-01-23,"Vancouver Coastal",2,2,0,24
#2020-01-23,"Vancouver Island",0,0,0,0
#2020-01-25,"BC",4,6,0,60
#2020-01-25,"Fraser",3,3,0,64

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

def bccdc_lab_info_charts():

    data_x_y = {}
    region_list = {}
    report_days = set()
    new_tests = {}
    total_tests = {}
    positivity = {}

    with open("../data/BCCDC_COVID19_Dashboard_Lab_Information.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            report_days.add(row_data["Date"])
            if row_data["Region"] != "BC":
                year_week = bc_report_date_to_year_week(row_data["Date"])
                if (year_week,row_data["Region"]) not in data_x_y:
                    data_x_y[(year_week,row_data["Region"])] = 0
                data_x_y[(year_week,row_data["Region"])] += int(row_data["New_Tests"]) 
                if row_data["Region"] not in region_list:
                    region_list[row_data["Region"]] = 0 
                region_list[row_data["Region"]] += int(row_data["New_Tests"]) 
                new_tests[(row_data["Date"],row_data["Region"])] = int(row_data["New_Tests"])
                positivity[(row_data["Date"],row_data["Region"])] = float(row_data["Positivity"])
                total_tests[(row_data["Date"],row_data["Region"])] = int(row_data["Total_Tests"])

    sorted_regions = sorted(region_list.keys(),key=lambda ha : -region_list[ha])
    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart1 = pygal.StackedBar(height=400, show_x_labels=True, show_legend=True,
    legend_at_bottom=False, x_title="Week number")
    for ha in sorted_regions:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week,ha) in data_x_y:
                timeseries_data.append(data_x_y[(week,ha)])
            else:
                timeseries_data.append(None)
        chart1.add({"title": ha}, timeseries_data)
                              
    chart1.title = "BC Weekly New Tests by Region"
    chart1.x_labels = [ w[1] for w in sorted_report_weeks ] 
    chart1.render_to_file('bccdc_weekly_lab_info_by_region_chart1.svg')

    sorted_report_days = sorted(report_days)
    chart1 = pygal.StackedBar(height=400,show_x_labels=True,x_label_rotation=0.01, 
        show_legend=True,show_minor_x_labels=False)
    for ha in sorted_regions:
        lab_info_per_day = []
        for day in sorted_report_days:
            if (day,ha) in new_tests:
                lab_info_per_day.append(new_tests[(day,ha)])
            else:
                lab_info_per_day.append(None)
        chart1.add(ha, lab_info_per_day)
    chart1.title = "Daily Tests by Region"
    chart1.x_labels = sorted_report_days 
    chart1.x_labels_major = [day for day in sorted_report_days if day[8:] == "01" ]
    chart1.render_to_file('bccdc_daily_new_tests_from_lab_info_by_region_chart1.svg')

    sorted_report_days = sorted(report_days)
    chart2 = pygal.Bar(height=400,show_x_labels=True,x_label_rotation=0.01, #dots_size=1, 
        show_legend=True,show_minor_x_labels=False)
    for ha in sorted_regions:
        lab_info_per_day = []
        for day in sorted_report_days:
            if (day,ha) in positivity:
                lab_info_per_day.append(positivity[(day,ha)])
            else:
                lab_info_per_day.append(None)
        chart2.add(ha, lab_info_per_day)
    chart2.title = "Daily Tests by Region"
    chart2.x_labels = sorted_report_days 
    chart2.x_labels_major = [day for day in sorted_report_days if day[8:] == "01" ]
    chart2.render_to_file('bccdc_daily_positivity_by_region_from_lab_info_line_chart2.svg')

    sorted_report_days = sorted(report_days)
    chart3 = pygal.Line(height=400,show_x_labels=True,x_label_rotation=0.01, #dots_size=1, 
        show_legend=True,show_minor_x_labels=False)
    for ha in sorted_regions:
        lab_info_per_day = []
        for day in sorted_report_days:
            if (day,ha) in total_tests:
                lab_info_per_day.append(total_tests[(day,ha)])
            else:
                lab_info_per_day.append(None)
        chart3.add(ha, lab_info_per_day)
    chart3.title = "Daily Tests by Region"
    chart3.x_labels = sorted_report_days 
    chart3.x_labels_major = [day for day in sorted_report_days if day[8:] == "01" ]
    chart3.render_to_file('bccdc_daily_total_tests_by_region_from_lab_info_line_chart3.svg')

    chart4 = pygal.Bar(height=400, show_legend=True)
    for ha in sorted_regions:
        chart4.add(ha, [ region_list[ha] ])
    chart4.title = "BC reported Tests by Region"
    chart4.x_labels = ["ha"]
    chart4.render_to_file('bccdc_lab_info_by_region_bar_chart4.svg')

    chart5 = pygal.Bar(height=400,show_legend=True)
    last_report_day = sorted_report_days[-1]
    for ha in sorted_regions:
        lab_info_per_day = []
        for day in [ last_report_day ]:
            if (day,ha) in new_tests:
                lab_info_per_day.append(positivity[(day,ha)])
            else:
                lab_info_per_day.append(None)
        chart5.add(ha, lab_info_per_day)
    chart5.title = "Last Reported Day {} Positivity by Region".format(last_report_day)
    chart5.render_to_file('bccdc_last_report_day_positivity_by_region_bar_chart5.svg')

if __name__ == "__main__":
    bccdc_lab_info_charts()
