import requests

files_list = [ "timeseries_canada/cases_timeseries_canada.csv", 
               "timeseries_canada/testing_timeseries_canada.csv",
               "timeseries_canada/mortality_timeseries_canada.csv",
               "timeseries_canada/active_timeseries_canada.csv",
               "timeseries_prov/cases_timeseries_prov.csv",
               "timeseries_prov/mortality_timeseries_prov.csv",
               "timeseries_prov/testing_timeseries_prov.csv"
               "timeseries_prov/active_timeseries_prov.csv",
               "timeseries_hr/cases_timeseries_hr.csv" , 
               "timeseries_hr/mortality_timeseries_hr.csv" ]

for csv_file in files_list:
    url = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/' + csv_file
    r = requests.get(url)
    with open('data/Covid19Canada/' + csv_file, 'wb') as f:
        f.write(r.content)

