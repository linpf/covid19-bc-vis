import requests

url = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Case_Details.csv'
r = requests.get(url)
with open('data/BCCDC_COVID19_Dashboard_Case_Details.csv', 'wb') as f:
    f.write(r.content)

url = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Lab_Information.csv'
r = requests.get(url)
with open('data/BCCDC_COVID19_Dashboard_Lab_Information.csv', 'wb') as f:
    f.write(r.content)

url = 'https://github.com/ishaberry/Covid19Canada/blob/master/timeseries_hr/cases_timeseries_hr.csv'
r = requests.get(url)
with open('cases_timeseries_hr.csv', 'wb') as f:
    f.write(r.content)
