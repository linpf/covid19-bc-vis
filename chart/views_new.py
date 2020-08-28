import pygal
from pygal.style import DarkSolarizedStyle
import csv
from collections import Counter
from django.shortcuts import render
from django.views.decorators.cache import cache_page
import datetime


@cache_page(60 * 15)
def home_view(request):

    return bc_cases_and_mortality_view(request)


@cache_page(60 * 15)
def bc_cases_by_age_group_view(request, end_date=None):

    charts = bccdc_cases_by_age_group_charts(request, end_date)
    context = {
        "charts": charts,
    }

    return render(request, "chart/charts.html", context)


@cache_page(60 * 15)
def bc_cases_by_sex_view(request):

    charts = bccdc_cases_by_sex_charts()

    context = {
        "charts": charts,
    }

    return render(request, "chart/charts.html", context)


@cache_page(60 * 15)
def bc_cases_by_ha_view(request):

    charts = bccdc_cases_by_ha_charts(request)
    context = {
        "charts": charts,
    }

    return render(request, "chart/charts.html", context)


@cache_page(60 * 15)
def bc_cases_and_mortality_view(request, end_date=None):

    charts = bccdc_cases_and_mortality_charts(request, end_date)
    context = {
        "charts": charts,
    }

    return render(request, "chart/charts.html", context)


@cache_page(60 * 15)
def bc_ha_cases_and_mortality_view(request, ha, end_date=None):

    charts = bccdc_ha_cases_and_mortality_charts(request, ha, end_date)
    context = {
        "charts": charts,
    }

    return render(request, "chart/charts.html", context)


@cache_page(60 * 15)
def bc_cases_and_testing_by_ha_view(request, ha=None, start_date=None, end_date=None):

    charts = bccdc_cases_and_testing_by_ha_charts(
        request, ha, start_date, end_date)
    context = {
        "charts": charts,
    }

    return render(request, "chart/charts.html", context)


@cache_page(60 * 15)
def bc_lab_tests_view(request, region=None, start_date=None, end_date=None):

    charts = bccdc_lab_tests_charts(request, region, start_date, end_date)
    context = {
        "charts": charts,
    }

    return render(request, "chart/charts.html", context)


@cache_page(60 * 15)
def bc_lab_tests_before_view(request, region, end_date):

    charts = bccdc_lab_tests_charts(request, region, None, end_date)

    context = {
        "charts": charts,
    }

    return render(request, "chart/charts.html", context)


def bccdc_cases_by_age_group_charts(request, end_date=None):

    l = []
    age_l = []
    data_x_y = {}
    age_groups_list = {}
    report_days = set()

    with open("data/BCCDC_COVID19_Dashboard_Case_Details.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if (end_date == None or from_new_report_format(row_data["Reported_Date"]) <= end_date):
                l.append((from_new_report_format(row_data["Reported_Date"]), row_data["Age_Group"]))
                age_l.append(row_data["Age_Group"])
                report_days.add(from_new_report_format(row_data["Reported_Date"]))
                year_week = bc_report_date_to_year_week(
                    from_new_report_format(row_data["Reported_Date"]))
                if (year_week, row_data["Age_Group"]) not in data_x_y:
                    data_x_y[(year_week, row_data["Age_Group"])] = 0
                data_x_y[(year_week, row_data["Age_Group"])] += 1
                if row_data["Age_Group"] not in age_groups_list:
                    age_groups_list[row_data["Age_Group"]] = 0
                age_groups_list[row_data["Age_Group"]] += 1

    sorted_age_groups = sorted(age_groups_list.keys())
    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart1 = pygal.StackedBar(height=400, show_x_labels=True, show_legend=False,
                              legend_at_bottom=False, x_title="Week number")
    for age_group in sorted_age_groups:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week, age_group) in data_x_y:
                timeseries_data.append(data_x_y[(week, age_group)])
            else:
                timeseries_data.append(None)
        chart1.add({"title": age_group}, timeseries_data)

    chart1.title = "BC Weekly New Cases by Age Group"
    chart1.x_labels = [w[1] for w in sorted_report_weeks]

    count = Counter(l)
    age_count = Counter(age_l)

    sorted_age = sorted(age_count.keys())
    sorted_report_days = sorted(report_days)
    chart2 = pygal.StackedBar(height=400, show_x_labels=True, x_label_rotation=0.01,
                              show_legend=False, show_minor_x_labels=False)
    for age in sorted_age:
        cases_per_day = []
        for day in sorted_report_days:
            if (day, age) in count:
                cases_per_day.append({'value': count[(day, age)], 'xlink': {"href": request.build_absolute_uri(
                    '/bc_cases_by_age_group/' + day + '/'), "target": "_top"}})
            else:
                cases_per_day.append(None)
        chart2.add(age, cases_per_day)
    chart2.title = "Daily Cases by Age Group"
    chart2.x_labels = sorted_report_days
    chart2.x_labels_major = [
        day for day in sorted_report_days if day[8:] == "01"]

    chart3 = pygal.HorizontalBar(
        height=400, show_x_labels=True, show_legend=True)
    for age in sorted_age:
        chart3.add(age, [age_count[age]])
    chart3.title = "\nBC Total reported Cases by Age Group\n"

    chart4 = pygal.HorizontalBar(
        height=400, show_legend=True, show_x_labels=True)
    last_report_week = sorted_report_weeks[-1]
    for age_group in sorted_age_groups:
        timeseries_data = []
        for week in [last_report_week]:
            if (week, age_group) in data_x_y:
                timeseries_data.append(data_x_y[(week, age_group)])
            else:
                timeseries_data.append(None)
        chart4.add({"title": age_group}, timeseries_data)

    year_week_str = str(last_report_week[0]) + ' ' + str(last_report_week[1])
    start_date_of_week = str(datetime.datetime.strptime(
        year_week_str+' 1', '%G %V %u'))[:10]
    end_date_of_week = str(datetime.datetime.strptime(
        year_week_str+' 7', '%G %V %u'))[:10]
    chart4.title = "BC Cases by Age Group in New Reported Week\n{} - {}\n{}".format(
        start_date_of_week, end_date_of_week, sorted_report_days[-1])

    return [chart2.render_data_uri(), chart1.render_data_uri(), chart3.render_data_uri(), chart4.render_data_uri()]


def bccdc_cases_by_sex_charts():

    l = []
    sex_l = []
    data_x_y = {}
    sexs_list = {}
    report_days = set()

    with open("data/BCCDC_COVID19_Dashboard_Case_Details.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            l.append((from_new_report_format(row_data["Reported_Date"]), row_data["Sex"]))
            sex_l.append(row_data["Sex"])
            report_days.add(from_new_report_format(row_data["Reported_Date"]))
            year_week = bc_report_date_to_year_week(from_new_report_format(row_data["Reported_Date"]))
            if (year_week, row_data["Sex"]) not in data_x_y:
                data_x_y[(year_week, row_data["Sex"])] = 0
            data_x_y[(year_week, row_data["Sex"])] += 1
            if row_data["Sex"] not in sexs_list:
                sexs_list[row_data["Sex"]] = 0
            sexs_list[row_data["Sex"]] += 1

    sorted_sexs = sorted(sexs_list.keys())

    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart1 = pygal.StackedBar(height=400, show_x_labels=True, show_legend=True,
                              legend_at_bottom=False, x_title="Week number")
    for sex in sorted_sexs:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week, sex) in data_x_y:
                timeseries_data.append(data_x_y[(week, sex)])
            else:
                timeseries_data.append(None)
        chart1.add({"title": sex}, timeseries_data)

    chart1.title = "BC Weekly New Cases by Sex"
    chart1.x_labels = [w[1] for w in sorted_report_weeks]

    count = Counter(l)
    sex_count = Counter(sex_l)

    sorted_sex = sorted(sex_count.keys())

    sorted_report_days = sorted(report_days)
    chart2 = pygal.StackedBar(height=400, show_x_labels=True, x_label_rotation=0.01,
                              show_legend=True, show_minor_x_labels=False)
    for sex in sorted_sex:
        cases_per_day = []
        for day in sorted_report_days:
            if (day, sex) in count:
                cases_per_day.append(count[(day, sex)])
            else:
                cases_per_day.append(None)
        chart2.add(sex, cases_per_day)
    chart2.title = "Daily Cases by Sex"
    chart2.x_labels = sorted_report_days
    chart2.x_labels_major = [
        day for day in sorted_report_days if day[8:] == "01"]

    chart3 = pygal.Pie(height=400, show_x_labels=True, show_legend=True)
    for sex in sorted_sex:
        chart3.add(sex, [sex_count[sex]])
    chart3.title = "BC Total reported Cases by Sex"

    chart4 = pygal.Pie(height=400, show_legend=True, show_x_labels=True)
    last_report_week = sorted_report_weeks[-1]
    for sex in sorted_sexs:
        timeseries_data = []
        for week in [last_report_week]:
            if (week, sex) in data_x_y:
                timeseries_data.append(data_x_y[(week, sex)])
            else:
                timeseries_data.append(None)
        chart4.add({"title": sex}, timeseries_data)
    year_week_str = str(last_report_week[0]) + ' ' + str(last_report_week[1])
    start_date_of_week = str(datetime.datetime.strptime(
        year_week_str+' 1', '%G %V %u'))[:10]
    end_date_of_week = str(datetime.datetime.strptime(
        year_week_str+' 7', '%G %V %u'))[:10]
    chart4.title = "BC Cases by Sex in New Reported Week\n{} - {}\n{}".format(
        start_date_of_week, end_date_of_week, sorted_report_days[-1])

    return [chart2.render_data_uri(), chart1.render_data_uri(), chart3.render_data_uri(), chart4.render_data_uri()]


def bccdc_ha_cases_and_mortality_charts(request, ha, end_date=None):

    l = []
    data_x_y = {}
    report_days = set()

    with open("data/BCCDC_COVID19_Dashboard_Case_Details.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if (end_date == None or from_new_report_format(row_data["Reported_Date"]) <= end_date):
                report_days.add(from_new_report_format(row_data["Reported_Date"]))
                if row_data["HA"] == ha:
                    l.append((from_new_report_format(row_data["Reported_Date"]), "cases"))
                    
                    year_week = bc_report_date_to_year_week(
                        from_new_report_format(row_data["Reported_Date"]))
                    if (year_week, "cases") not in data_x_y:
                        data_x_y[(year_week, "cases")] = 0
                    data_x_y[(year_week, "cases")] += 1

    count = Counter(l)

    hr = ha if ha != "Vancouver Island" else "Island"
    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if (end_date == None or bc_report_day(row_data["date_death_report"]) <= end_date):
                if row_data["health_region"] == hr and row_data["province"] == "BC":
                    #report_days.add(bc_report_day(row_data["date_death_report"]))
                    year_week = report_date_to_year_week(
                        row_data["date_death_report"])
                    if (year_week, "deaths") not in data_x_y:
                        data_x_y[(year_week, "deaths")] = 0
                    data_x_y[(year_week, "deaths")] += int(row_data["deaths"])
                    count[(bc_report_day(row_data["date_death_report"]), "deaths")] = int(
                        row_data["deaths"])

    with open("data/BCCDC_COVID19_Dashboard_Lab_Information.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if (end_date == None or row_data["Date"] <= end_date):
                if row_data["Region"] == ha:
                    year_week = bc_report_date_to_year_week(row_data["Date"])
                    if (year_week, "testing") not in data_x_y:
                        data_x_y[(year_week, "testing")] = 0
                    data_x_y[(year_week, "testing")
                             ] += int(row_data["New_Tests"])

    sorted_report_days = sorted(report_days)
    chart1 = pygal.Bar(height=400, show_x_labels=True, x_label_rotation=0.01,
                       show_legend=True, show_minor_x_labels=False, legend_at_bottom=True)
    for data in ["deaths", "cases"]:
        cases_per_day = []
        for day in sorted_report_days:
            if (day, data) in count:
                cases_per_day.append(count[(day, data)])
            else:
                cases_per_day.append(None)
        chart1.add(data, cases_per_day)
    chart1.title = "{} Cases and Deaths by Day".format(ha)
    chart1.x_labels = sorted_report_days
    chart1.x_labels_major = [
        day for day in sorted_report_days if day[8:] == "01"]

    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart2 = pygal.Bar(height=400, show_x_labels=True, show_legend=True,
                       legend_at_bottom=True, x_title="Week number")
    for data in ["deaths", "cases"]:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week, data) in data_x_y:
                timeseries_data.append(data_x_y[(week, data)])
            else:
                timeseries_data.append(None)
        chart2.add({"title": data}, timeseries_data)

    chart2.title = "{} Cases and Deaths by Week".format(ha)
    chart2.x_labels = [w[1] for w in sorted_report_weeks]

    chart4 = pygal.Bar(height=400, show_x_labels=True, show_legend=True,
                       legend_at_bottom=True, x_title="Week number")
    for data in ["testing", "cases"]:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week, data) in data_x_y:
                timeseries_data.append(data_x_y[(week, data)])
            else:
                timeseries_data.append(None)
        if data == "testing":
            chart4.add({"title": data, 'xlink': {"href": request.build_absolute_uri(
                '/bc_lab_tests_before/' + ha + '/' + day + '/'), "target": "_top"}}, timeseries_data)
        else:
            chart4.add({"title": data}, timeseries_data)
        #chart4.add({"title": data}, timeseries_data)

    chart4.title = "{} Cases and Testing by Week".format(ha)
    chart4.x_labels = [w[1] for w in sorted_report_weeks]

    chart3 = pygal.HorizontalBar(
        height=400, show_legend=True, show_x_labels=True, legend_at_bottom=True)
    last_report_week = sorted_report_weeks[-1]
    for data in ["deaths", "cases"]:
        timeseries_data = []
        for week in [last_report_week]:
            if (week, data) in data_x_y:
                timeseries_data.append(data_x_y[(week, data)])
            else:
                timeseries_data.append(None)
        chart3.add({"title": data}, timeseries_data)

    year_week_str = str(last_report_week[0]) + ' ' + str(last_report_week[1])
    start_date_of_week = str(datetime.datetime.strptime(
        year_week_str+' 1', '%G %V %u'))[:10]
    end_date_of_week = str(datetime.datetime.strptime(
        year_week_str+' 7', '%G %V %u'))[:10]
    chart3.title = "{} Cases and Deaths in New Reported Week\n{} - {}\n{}".format(
        ha, start_date_of_week, end_date_of_week, sorted_report_days[-1])

    return [chart1.render_data_uri(), chart2.render_data_uri(), chart3.render_data_uri(), chart4.render_data_uri()]


def bccdc_cases_and_mortality_charts(request, end_date=None):

    l = []
    data_x_y = {}
    report_days = set()

    with open("data/BCCDC_COVID19_Dashboard_Case_Details.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if (end_date == None or from_new_report_format(row_data["Reported_Date"]) <= end_date):
                l.append((from_new_report_format(row_data["Reported_Date"]), "cases"))
                report_days.add(from_new_report_format(row_data["Reported_Date"]))
                year_week = bc_report_date_to_year_week(
                    from_new_report_format(row_data["Reported_Date"]))
                if (year_week, "cases") not in data_x_y:
                    data_x_y[(year_week, "cases")] = 0
                data_x_y[(year_week, "cases")] += 1

    count = Counter(l)

    with open("data/Covid19Canada/timeseries_prov/mortality_timeseries_prov.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if (end_date == None or bc_report_day(row_data["date_death_report"]) <= end_date):
                if row_data["province"] == "BC":
                    #report_days.add(bc_report_day(row_data["date_death_report"]))
                    year_week = report_date_to_year_week(
                        row_data["date_death_report"])
                    if (year_week, "deaths") not in data_x_y:
                        data_x_y[(year_week, "deaths")] = 0
                    data_x_y[(year_week, "deaths")] += int(row_data["deaths"])
                    count[(bc_report_day(row_data["date_death_report"]), "deaths")] = int(
                        row_data["deaths"])

    with open("data/BCCDC_COVID19_Dashboard_Lab_Information.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if (end_date == None or row_data["Date"] <= end_date):
                if row_data["Region"] == "BC":
                    year_week = bc_report_date_to_year_week(row_data["Date"])
                    if (year_week, "testing") not in data_x_y:
                        data_x_y[(year_week, "testing")] = 0
                    data_x_y[(year_week, "testing")
                             ] += int(row_data["New_Tests"])

    sorted_report_days = sorted(report_days)
    chart1 = pygal.Bar(height=400, show_x_labels=True, x_label_rotation=0.01,
                       show_legend=True, show_minor_x_labels=False, legend_at_bottom=True)
    for data in ["deaths", "cases"]:
        cases_per_day = []
        for day in sorted_report_days:
            if (day, data) in count:
                cases_per_day.append({"value": count[(day, data)], 'xlink': {"href": request.build_absolute_uri(
                    '/bc_cases_and_mortality/' + day + '/'), "target": "_top"}})
            else:
                cases_per_day.append(None)
        chart1.add(data, cases_per_day)
    chart1.title = "BC Cases and Deaths by Day"
    chart1.x_labels = sorted_report_days
    chart1.x_labels_major = [
        day for day in sorted_report_days if day[8:] == "01"]

    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart2 = pygal.Bar(height=400, show_x_labels=True, show_legend=True,
                       legend_at_bottom=True, x_title="Week number")
    for data in ["deaths", "cases"]:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week, data) in data_x_y:
                timeseries_data.append(data_x_y[(week, data)])
            else:
                timeseries_data.append(None)
        chart2.add({"title": data}, timeseries_data)

    chart2.title = "BC Cases and Deaths by Week"
    chart2.x_labels = [w[1] for w in sorted_report_weeks]

    chart4 = pygal.Bar(height=400, show_x_labels=True, show_legend=True,
                       legend_at_bottom=True, x_title="Week number")
    for data in ["testing", "cases"]:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week, data) in data_x_y:
                timeseries_data.append(data_x_y[(week, data)])
            else:
                timeseries_data.append(None)
        if data == "testing":
            chart4.add({"title": data, 'xlink': {"href": request.build_absolute_uri(
                '/bc_lab_tests_before/HA/' + day + '/'), "target": "_top"}}, timeseries_data)
        else:
            chart4.add({"title": data}, timeseries_data)

    chart4.title = "BC Cases and Testing by Week"
    chart4.x_labels = [w[1] for w in sorted_report_weeks]

    data_x_y = {}
    deaths_x_y = {}
    has_list = {}

    with open("data/BCCDC_COVID19_Dashboard_Case_Details.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if (end_date == None or from_new_report_format(row_data["Reported_Date"]) <= end_date):
                year_week = bc_report_date_to_year_week(
                    from_new_report_format(row_data["Reported_Date"]))
                if (year_week, row_data["HA"]) not in data_x_y:
                    data_x_y[(year_week, row_data["HA"])] = 0
                data_x_y[(year_week, row_data["HA"])] += 1
                if row_data["HA"] not in has_list:
                    has_list[row_data["HA"]] = 0
                has_list[row_data["HA"]] += 1

    with open("data/Covid19Canada/timeseries_hr/mortality_timeseries_hr.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if (end_date == None or bc_report_day(row_data["date_death_report"]) <= end_date):
                if row_data["province"] == "BC":
                    year_week = report_date_to_year_week(
                        row_data["date_death_report"])
                    if (year_week, row_data["health_region"]) not in deaths_x_y:
                        deaths_x_y[(year_week, row_data["health_region"])] = 0
                    deaths_x_y[(year_week, row_data["health_region"])
                               ] += int(row_data["deaths"])

    sorted_has = sorted(has_list.keys(), key=lambda ha: -has_list[ha])

    chart3 = pygal.HorizontalStackedBar(
        height=400, show_legend=True, show_x_labels=True, legend_at_bottom=True)
    last_report_week = sorted_report_weeks[-1]
    year_week_str = str(last_report_week[0]) + ' ' + str(last_report_week[1])
    start_date_of_week = str(datetime.datetime.strptime(
        year_week_str+' 1', '%G %V %u'))[:10]
    end_date_of_week = str(datetime.datetime.strptime(
        year_week_str+' 7', '%G %V %u'))[:10]
    for ha in sorted_has:
        timeseries_data = []
        hr = ha if ha != "Vancouver Island" else "Island"
        for week in [last_report_week]:
            if (week, hr) in deaths_x_y:
                timeseries_data.append(deaths_x_y[(week, hr)])
            else:
                timeseries_data.append(None)
            if (week, ha) in data_x_y:
                timeseries_data.append(data_x_y[(week, ha)])
            else:
                timeseries_data.append(None)
        if end_date == None:
            chart3.add({"title": ha, 'xlink': {"href": request.build_absolute_uri(
                '/bc_ha_cases_and_mortality/' + ha + '/'), "target": "_top"}}, timeseries_data)
        else:
            chart3.add({"title": ha, 'xlink': {"href": request.build_absolute_uri(
                '/bc_ha_cases_and_mortality/' + ha + '/' + end_date + '/'), "target": "_top"}}, timeseries_data)
    chart3.title = "BC Cases by Health Authority in New Reported Week\n{} - {}\n{}".format(
        start_date_of_week, end_date_of_week, sorted_report_days[-1])
    chart3.x_labels = ["deaths", "cases"]
    return [chart1.render_data_uri(), chart2.render_data_uri(), chart3.render_data_uri(), chart4.render_data_uri()]


def bccdc_cases_by_ha_charts(request, ha=None):

    l = []
    ha_l = []
    data_x_y = {}
    has_list = {}
    report_days = set()

    with open("data/BCCDC_COVID19_Dashboard_Case_Details.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if ha == None:
                l.append((from_new_report_format(row_data["Reported_Date"]), row_data["HA"]))
                ha_l.append(row_data["HA"])
                report_days.add(from_new_report_format(row_data["Reported_Date"]))
                year_week = bc_report_date_to_year_week(
                    from_new_report_format(row_data["Reported_Date"]))
                if (year_week, row_data["HA"]) not in data_x_y:
                    data_x_y[(year_week, row_data["HA"])] = 0
                data_x_y[(year_week, row_data["HA"])] += 1
                if row_data["HA"] not in has_list:
                    has_list[row_data["HA"]] = 0
                has_list[row_data["HA"]] += 1
            elif row_data["HA"] == ha:
                l.append((from_new_report_format(row_data["Reported_Date"]), row_data["HA"]))
                ha_l.append(row_data["HA"])
                report_days.add(from_new_report_format(row_data["Reported_Date"]))
                year_week = bc_report_date_to_year_week(
                    from_new_report_format(row_data["Reported_Date"]))
                if (year_week, row_data["HA"]) not in data_x_y:
                    data_x_y[(year_week, row_data["HA"])] = 0
                data_x_y[(year_week, row_data["HA"])] += 1
                if row_data["HA"] not in has_list:
                    has_list[row_data["HA"]] = 0
                has_list[row_data["HA"]] += 1

    sorted_has = sorted(has_list.keys(), key=lambda ha: -has_list[ha])

    report_weeks = set()
    for key in data_x_y:
        week = key[0]
        report_weeks.add(week)

    sorted_report_weeks = sorted(report_weeks)
    chart1 = pygal.StackedBar(height=400, show_x_labels=True, show_legend=False,
                              legend_at_bottom=True, x_title="Week number")
    for ha in sorted_has:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week, ha) in data_x_y:
                timeseries_data.append(data_x_y[(week, ha)])
            else:
                timeseries_data.append(None)
        chart1.add({"title": ha}, timeseries_data)

    chart1.title = "Health Authority Cases Reported to Public Health by Week"
    chart1.x_labels = [w[1] for w in sorted_report_weeks]

    count = Counter(l)
    ha_count = Counter(ha_l)

    sorted_report_days = sorted(report_days)
    chart2 = pygal.StackedBar(height=400, show_x_labels=True, x_label_rotation=0.01,
                              show_legend=True, show_minor_x_labels=False, legend_at_bottom=True)
    for ha in sorted_has:
        cases_per_day = []
        for day in sorted_report_days:
            if (day, ha) in count:
                cases_per_day.append(count[(day, ha)])
            else:
                cases_per_day.append(None)
        chart2.add(ha, cases_per_day)
    chart2.title = "Health Authority Cases Reported to Public Health by Day"
    chart2.x_labels = sorted_report_days
    chart2.x_labels_major = [
        day for day in sorted_report_days if day[8:] == "01"]

    chart3 = pygal.HorizontalStackedBar(
        height=400, show_legend=True, legend_at_bottom=True)
    chart3.title = "\nHealth Authority Total Cases Reported to Public Health\n"
    for ha in sorted_has:
        chart3.add(ha, [ha_count[ha]])


    chart4 = pygal.HorizontalStackedBar(
        height=400, show_legend=True, show_x_labels=True, legend_at_bottom=True)
    last_report_week = sorted_report_weeks[-1]
    for ha in sorted_has:
        timeseries_data = []
        for week in [last_report_week]:
            if (week, ha) in data_x_y:
                timeseries_data.append(data_x_y[(week, ha)])
            else:
                timeseries_data.append(None)
        chart4.add({"title": ha}, timeseries_data)

    year_week_str = str(last_report_week[0]) + ' ' + str(last_report_week[1])
    start_date_of_week = str(datetime.datetime.strptime(
        year_week_str+' 1', '%G %V %u'))[:10]
    end_date_of_week = str(datetime.datetime.strptime(
        year_week_str+' 7', '%G %V %u'))[:10]
    chart4.title = "Cases by Health Authority in New Reported Week\n{} - {}\n{}".format(
        start_date_of_week, end_date_of_week, sorted_report_days[-1])

    return [chart2.render_data_uri(), chart1.render_data_uri(), chart3.render_data_uri(), chart4.render_data_uri()]


def bccdc_cases_and_testing_by_ha_charts(request, ha=None, start_date=None, end_date=None):

    region_list = {}
    report_days = set()
    new_tests = {}
    region = ha
    total_tests = {}
    new_tests_by_week = {}
    
    with open("data/BCCDC_COVID19_Dashboard_Lab_Information.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if ((start_date == None or row_data["Date"] >= start_date) and (end_date == None or row_data["Date"] <= end_date)):
                if region == None or region == "HA":
                    if row_data["Region"] != "BC":
                        report_days.add(row_data["Date"])
                        if row_data["Region"] not in region_list:
                            region_list[row_data["Region"]] = 0
                        region_list[row_data["Region"]
                                    ] += int(row_data["New_Tests"])
                        new_tests[(row_data["Date"], row_data["Region"])] = int(
                            row_data["New_Tests"])
                        total_tests[(row_data["Date"], row_data["Region"])] = int(
                            row_data["Total_Tests"])
                            
                        year_week = bc_report_date_to_year_week(row_data["Date"])
                        new_tests_by_week[(year_week, row_data["Region"])] = int(
                            row_data["New_Tests"]) + new_tests_by_week.get((year_week, row_data["Region"]),0)
                            
                else:
                    if row_data["Region"] == region:
                        report_days.add(row_data["Date"])
                        if row_data["Region"] not in region_list:
                            region_list[row_data["Region"]] = 0
                        region_list[row_data["Region"]
                                    ] += int(row_data["New_Tests"])
                        new_tests[(row_data["Date"], row_data["Region"])] = int(
                            row_data["New_Tests"])
                        total_tests[(row_data["Date"], row_data["Region"])] = int(
                            row_data["Total_Tests"])
                        
                        year_week = bc_report_date_to_year_week(row_data["Date"])
                        new_tests_by_week[(year_week, row_data["Region"])] = int(
                            row_data["New_Tests"]) + new_tests_by_week.get((year_week, row_data["Region"]),0)

    l = []
    ha_l = []
    has_list = {}
    data_x_y = {}
    new_cases_by_week = {}

    with open("data/BCCDC_COVID19_Dashboard_Case_Details.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if ((start_date == None or from_new_report_format(row_data["Reported_Date"]) >= start_date) and (end_date == None or row_data["Reported_Date"] <= end_date)):
                if ha == None or ha == "HA":
                    l.append((from_new_report_format(row_data["Reported_Date"]), row_data["HA"]))
                    ha_l.append(row_data["HA"])
                    report_days.add(from_new_report_format(row_data["Reported_Date"]))
                    if row_data["HA"] not in has_list:
                        has_list[row_data["HA"]] = 0
                    has_list[row_data["HA"]] += 1
                    
                    year_week = bc_report_date_to_year_week(
                        from_new_report_format(row_data["Reported_Date"]))
                    if (year_week, row_data["HA"]) not in new_cases_by_week:
                        new_cases_by_week[(year_week, row_data["HA"])] = 0
                    new_cases_by_week[(year_week, row_data["HA"])] += 1
                    
                    
                elif ha == "BC":
                    l.append((from_new_report_format(row_data["Reported_Date"]), "BC"))
                    ha_l.append("BC")
                    report_days.add(from_new_report_format(row_data["Reported_Date"]))
                    if "BC" not in has_list:
                        has_list["BC"] = 0
                    has_list["BC"] += 1
                    
                    year_week = bc_report_date_to_year_week(
                        from_new_report_format(row_data["Reported_Date"]))
                    if (year_week, "BC") not in new_cases_by_week:
                        new_cases_by_week[(year_week, "BC")] = 0
                    new_cases_by_week[(year_week, "BC")] += 1
                    
                elif row_data["HA"] == ha:
                    l.append((from_new_report_format(row_data["Reported_Date"]), row_data["HA"]))
                    ha_l.append(row_data["HA"])
                    report_days.add(from_new_report_format(row_data["Reported_Date"]))
                    if row_data["HA"] not in has_list:
                        has_list[row_data["HA"]] = 0
                    has_list[row_data["HA"]] += 1
                    
                    year_week = bc_report_date_to_year_week(
                        from_new_report_format(row_data["Reported_Date"]))
                    if (year_week, row_data["HA"]) not in new_cases_by_week:
                        new_cases_by_week[(year_week, row_data["HA"])] = 0
                    new_cases_by_week[(year_week, row_data["HA"])] += 1
                    
                
    sorted_regions = sorted(
        region_list.keys(), key=lambda ha: -region_list[ha])

    sorted_report_days = sorted(report_days)
    chart1 = pygal.StackedBar(height=400, show_x_labels=True, x_label_rotation=0.01,
                              show_legend=False, show_minor_x_labels=False, legend_at_bottom=True)

    for ha in sorted_regions:
        lab_info_per_day = []
        for day in sorted_report_days:
            if (day, ha) in new_tests:
                lab_info_per_day.append({"value": new_tests[(day, ha)], 'xlink': {"href": request.build_absolute_uri(
                    '/bc_cases_and_testing_by_ha/' + region + '/' + day[:-2] + '01' + '/'), "target": "_top"}})
            else:
                lab_info_per_day.append(None)
        chart1.add({"title": ha, 'xlink': {"href": request.build_absolute_uri(
            '/bc_cases_and_testing_by_ha/' + ha + '/'), "target": "_top"}}, lab_info_per_day)
    chart1.title = "{} New Laboratory Tests Performed".format(
        region if region != 'HA' else '')
    chart1.x_labels = sorted_report_days
    chart1.x_labels_major = [
        day for day in sorted_report_days if day[8:] == "01"]
        
    report_weeks = set()
    for key in new_tests_by_week:
        week = key[0]
        report_weeks.add(week)
    
    sorted_report_weeks = sorted(report_weeks)
    chart1 = pygal.StackedBar(height=400, show_x_labels=True, show_legend=True,
                              legend_at_bottom=True, x_title="Week number")
    for ha in sorted_regions:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week, ha) in new_tests_by_week:
                timeseries_data.append(new_tests_by_week[(week, ha)])
            else:
                timeseries_data.append(None)
        chart1.add({"title": ha}, timeseries_data)

    chart1.title = "{} New Laboratory Tests Performed".format(
        region if region != 'HA' else '')
    chart1.x_labels = [w[1] for w in sorted_report_weeks]
    
    sorted_has = sorted(has_list.keys(), key=lambda ha: -
                        region_list.get(ha, 0))
    count = Counter(l)

    sorted_report_days = sorted(report_days)
    chart3 = pygal.StackedBar(height=400, show_x_labels=True, x_label_rotation=0.01,
                              show_legend=False, show_minor_x_labels=False, legend_at_bottom=True)
    for ha in sorted_has:
        cases_per_day = []
        for day in sorted_report_days:
            if (day, ha) in count:
                cases_per_day.append({"value": count[(day, ha)], 'xlink': {"href": request.build_absolute_uri(
                    '/bc_cases_and_testing_by_ha/' + region + '/' + day[:-2] + '01' + '/'), "target": "_top"}})
            else:
                cases_per_day.append(None)
        chart3.add({"title": ha, 'xlink': {"href": request.build_absolute_uri(
            '/bc_cases_and_testing_by_ha/' + ha + '/'), "target": "_top"}}, cases_per_day)
    chart3.title = "Health Authority Cases Reported to Public Health by Day"
    chart3.x_labels = sorted_report_days
    chart3.x_labels_major = [
        day for day in sorted_report_days if day[8:] == "01"]
        
    report_weeks = set()
    for key in new_cases_by_week:
        week = key[0]
        report_weeks.add(week)
    
    sorted_report_weeks = sorted(report_weeks)
    chart3 = pygal.StackedBar(height=400, show_x_labels=True, show_legend=True,
                              legend_at_bottom=True, x_title="Week number")
    for ha in sorted_has:
        timeseries_data = []
        for week in sorted_report_weeks:
            if (week, ha) in new_cases_by_week:
                timeseries_data.append(new_cases_by_week[(week, ha)])
            else:
                timeseries_data.append(None)
        chart3.add({"title": ha}, timeseries_data)

    chart3.title = "Health Authority Cases Reported to Public Health by Week"
    chart3.x_labels = [w[1] for w in sorted_report_weeks]
    
    sorted_report_days = sorted(report_days)
    chart2 = pygal.Line(height=400, show_x_labels=True, x_label_rotation=0.01,  # dots_size=2,
                        show_legend=True, show_minor_x_labels=False, legend_at_bottom=True)
    for ha in sorted_regions:
        lab_info_per_day = []
        for day in sorted_report_days:
            if (day, ha) in total_tests:
                lab_info_per_day.append(total_tests[(day, ha)])
            else:
                lab_info_per_day.append(None)
        chart2.add({"title": ha, 'xlink': {"href": request.build_absolute_uri(
            '/bc_lab_tests/' + ha + '/'), "target": "_top"}}, lab_info_per_day)
    chart2.title = "{} Total cumulative Laboratory Tests Performed by date".format(
        region if region != 'HA' else '')
    chart2.x_labels = sorted_report_days
    chart2.x_labels_major = [
        day for day in sorted_report_days if day[8:] == "01"]

    chart4 = pygal.Line(height=400, show_x_labels=True, x_label_rotation=0.01,  # dots_size=2,
                        show_legend=True, legend_at_bottom=True, show_minor_x_labels=False)
    for ha in sorted_has:
        cases_per_day = []
        accu_count = 0
        for day in sorted_report_days:
            if (day, ha) in count:
                accu_count += count[(day, ha)]
            cases_per_day.append({"value": accu_count, 'xlink': {"href": request.build_absolute_uri(
                '/bc_cases_and_testing_by_ha/' + region + '/' + day[:-2] + '01' + '/'), "target": "_top"}})
        chart4.add({"title": ha, 'xlink': {"href": request.build_absolute_uri(
            '/bc_cases_and_testing_by_ha/' + ha + '/'), "target": "_top"}}, cases_per_day)
    chart4.title = "Health Authority Total Cases Reported to Public Health by Day"
    chart4.x_labels = sorted_report_days
    chart4.x_labels_major = [
        day for day in sorted_report_days if day[8:] == "01"]

    return [chart1.render_data_uri(), chart2.render_data_uri(), chart3.render_data_uri(), chart4.render_data_uri()]


def bccdc_lab_tests_charts(request, region=None, start_date=None, end_date=None):

    data_x_y = {}
    region_list = {}
    report_days = set()
    new_tests = {}
    total_tests = {}
    positivity = {}
    turn_around = {}

    with open("data/BCCDC_COVID19_Dashboard_Lab_Information.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if region == None or region == "HA":
                if row_data["Region"] != "BC":
                    if ((start_date == None or row_data["Date"] >= start_date) and (end_date == None or row_data["Date"] <= end_date)):
                        report_days.add(row_data["Date"])
                        year_week = bc_report_date_to_year_week(
                            row_data["Date"])
                        if (year_week, row_data["Region"]) not in data_x_y:
                            data_x_y[(year_week, row_data["Region"])] = 0
                        data_x_y[(year_week, row_data["Region"])
                                 ] += int(row_data["New_Tests"])
                        if row_data["Region"] not in region_list:
                            region_list[row_data["Region"]] = 0
                        region_list[row_data["Region"]
                                    ] += int(row_data["New_Tests"])
                        new_tests[(row_data["Date"], row_data["Region"])] = int(
                            row_data["New_Tests"])
                        positivity[(row_data["Date"], row_data["Region"])] = float(
                            row_data["Positivity"])
                        turn_around[(row_data["Date"], row_data["Region"])] = float(
                            row_data["Turn_Around"])
                        total_tests[(row_data["Date"], row_data["Region"])] = int(
                            row_data["Total_Tests"])
            else:
                if row_data["Region"] == region:
                    if ((start_date == None or row_data["Date"] >= start_date) and (end_date == None or row_data["Date"] <= end_date)):
                        report_days.add(row_data["Date"])
                        year_week = bc_report_date_to_year_week(
                            row_data["Date"])
                        if (year_week, row_data["Region"]) not in data_x_y:
                            data_x_y[(year_week, row_data["Region"])] = 0
                        data_x_y[(year_week, row_data["Region"])
                                 ] += int(row_data["New_Tests"])
                        if row_data["Region"] not in region_list:
                            region_list[row_data["Region"]] = 0
                        region_list[row_data["Region"]
                                    ] += int(row_data["New_Tests"])
                        new_tests[(row_data["Date"], row_data["Region"])] = int(
                            row_data["New_Tests"])
                        positivity[(row_data["Date"], row_data["Region"])] = float(
                            row_data["Positivity"])
                        turn_around[(row_data["Date"], row_data["Region"])] = float(
                            row_data["Turn_Around"])
                        total_tests[(row_data["Date"], row_data["Region"])] = int(
                            row_data["Total_Tests"])

    l = []
    ha_l = []
    has_list = {}
    ha = region

    with open("data/BCCDC_COVID19_Dashboard_Case_Details.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            row_data = dict(row)
            if ((start_date == None or from_new_report_format(row_data["Reported_Date"]) >= start_date) and (end_date == None or from_new_report_format(row_data["Reported_Date"]) <= end_date)):
                if ha == None or ha == "HA":
                    l.append((from_new_report_format(row_data["Reported_Date"]), row_data["HA"]))
                    ha_l.append(row_data["HA"])
                    report_days.add(from_new_report_format(row_data["Reported_Date"]))
                    if row_data["HA"] not in has_list:
                        has_list[row_data["HA"]] = 0
                    has_list[row_data["HA"]] += 1
                elif ha == "BC":
                    l.append((from_new_report_format(row_data["Reported_Date"]), "BC"))
                    ha_l.append("BC")
                    report_days.add(from_new_report_format(row_data["Reported_Date"]))
                    if "BC" not in has_list:
                        has_list["BC"] = 0
                    has_list["BC"] += 1
                elif row_data["HA"] == ha:
                    l.append((from_new_report_format(row_data["Reported_Date"]), row_data["HA"]))
                    ha_l.append(row_data["HA"])
                    report_days.add(from_new_report_format(row_data["Reported_Date"]))
                    if row_data["HA"] not in has_list:
                        has_list[row_data["HA"]] = 0
                    has_list[row_data["HA"]] += 1

    sorted_regions = sorted(
        region_list.keys(), key=lambda ha: -region_list[ha])

    sorted_report_days = sorted(report_days)

    chart4 = pygal.Bar(height=400, show_x_labels=True, x_label_rotation=0.01,  # dots_size=1,
                       show_legend=True, show_minor_x_labels=False, legend_at_bottom=True)
    for ha in sorted_regions:
        lab_info_per_day = []
        for day in sorted_report_days:
            if (day, ha) in positivity:
                lab_info_per_day.append({"value": positivity[(day, ha)], 'xlink': {"href": request.build_absolute_uri(
                    '/bc_lab_tests/' + region + '/' + sorted_report_days[0] + '/' + day + '/'), "target": "_top"}})
            else:
                lab_info_per_day.append(None)
        chart4.add({"title": ha}, lab_info_per_day)
    chart4.title = "{} % of test samples that are positive".format(
        region if region != 'HA' else '')
    chart4.x_labels = sorted_report_days
    chart4.x_labels_major = [
        day for day in sorted_report_days if day[8:] == "01"]

    chart1 = pygal.Bar(height=400, show_x_labels=True, x_label_rotation=0.01,
                       show_legend=True, show_minor_x_labels=False, legend_at_bottom=True)
    for ha in sorted_regions:
        lab_info_per_day = []
        for day in sorted_report_days:
            if (day, ha) in new_tests:
                lab_info_per_day.append({"value": new_tests[(day, ha)], 'xlink': {"href": request.build_absolute_uri(
                    '/bc_lab_tests/' + region + '/' + day[:-2] + '01' + '/'), "target": "_top"}})
            else:
                lab_info_per_day.append(None)
        chart1.add({"title": ha, 'xlink': {"href": request.build_absolute_uri(
            '/bc_lab_tests/' + ha + '/'), "target": "_top"}}, lab_info_per_day)
    chart1.title = "{} New Laboratory Tests Performed".format(
        region if region != 'HA' else '')
    chart1.x_labels = sorted_report_days
    chart1.x_labels_major = [
        day for day in sorted_report_days if day[8:] == "01"]

    chart2 = pygal.Bar(height=400, show_x_labels=True, x_label_rotation=0.01,  # dots_size=1,
                       show_legend=True, show_minor_x_labels=False, legend_at_bottom=True)
    for ha in sorted_regions:
        lab_info_per_day = []
        for day in sorted_report_days:
            if (day, ha) in turn_around:
                lab_info_per_day.append({'value': turn_around[(day, ha)],
                                         'xlink': {"href": request.build_absolute_uri('/bc_lab_tests/' + region + '/' + day + '/'), "target": "_top"}})
            else:
                lab_info_per_day.append(None)
        chart2.add({"title": ha}, lab_info_per_day)
    chart2.title = "{} Average Test Turn-Around Time (Hours)".format(
        region if region != 'HA' else '')
    chart2.x_labels = sorted_report_days
    chart2.x_labels_major = [
        day for day in sorted_report_days if day[8:] == "01"]

    sorted_has = sorted(has_list.keys(), key=lambda ha: -
                        region_list.get(ha, 0))
    count = Counter(l)

    sorted_report_days = sorted(report_days)
    chart3 = pygal.Bar(height=400, show_x_labels=True, x_label_rotation=0.01,
                       show_legend=True, show_minor_x_labels=False, legend_at_bottom=True)
    for ha in sorted_has:
        cases_per_day = []
        for day in sorted_report_days:
            if (day, ha) in count:
                cases_per_day.append({"value": count[(day, ha)], 'xlink': {"href": request.build_absolute_uri(
                    '/bc_lab_tests/' + region + '/' + sorted_report_days[0] + '/' + day[:-2] + '01' + '/'), "target": "_top"}})
            else:
                cases_per_day.append(None)
        chart3.add({"title": ha, 'xlink': {"href": request.build_absolute_uri(
            '/bc_lab_tests/' + ha + '/'), "target": "_top"}}, cases_per_day)
    chart3.title = "{} Cases Reported to Public Health by Day".format(
        region if region != 'HA' else '')
    chart3.x_labels = sorted_report_days
    chart3.x_labels_major = [
        day for day in sorted_report_days if day[8:] == "01"]

    return [chart1.render_data_uri(), chart2.render_data_uri(), chart3.render_data_uri(), chart4.render_data_uri()]



def bc_report_date_to_year_week(date):
    l = date.split("-")
    d = datetime.date(int(l[0]), int(l[1]), int(l[2]))
    cal = d.isocalendar()
    return cal[:2]


def bc_report_day(date):
    l = date.split("-")
    return l[2] + "-" + l[1] + "-" + l[0]


def day_month_year(date):
    l = date.split("-")
    return l[2] + l[1] + l[0]


def display_month_day(date):
    l = date.split("-")
    return date
    
def from_new_report_format(date):
    l = date.split("/")
    return "{:04d}-{:02d}-{:02d}".format(int(l[2]),int(l[0]),int(l[1])) 

def report_date_to_year_week(date):
    l = date.split("-")
    d = datetime.date(int(l[2]), int(l[1]), int(l[0]))
    cal = d.isocalendar()
    return cal[:2]
