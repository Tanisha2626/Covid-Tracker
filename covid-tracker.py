import pandas as pd
import requests
import csv
import webbrowser

covid_report_file = 'CovidReport.csv'
report_webpage = 'CovidReport.html'
covid_dumps_file = 'Resources\CovidDumps.csv'
# input_file = 'Test\\test.csv'
input_file = 'inputs.csv'

covidUrl = 'https://api.covid19india.org/csv/latest/district_wise.csv'
headers = {'authorization': "", 'accept': "text/csv"}

# API Call to retrieve report
results = requests.get(covidUrl, headers=headers)
data = results.text
# print(data)


def openWeb(report):
    # print('inside FUNK == ', report)
    webbrowser.open(report)


# Write API Results to file
fs = open(covid_dumps_file, "w")
fs.flush()
fs.write(data)
fs.close()

with open(covid_dumps_file, 'r') as covid_dumps:
    csv_reader = csv.DictReader(covid_dumps)
    myList = []

    for line in csv_reader:
        if(line['District'] != 'Unknown'):
            myList.append({'KEY': line['District_Key'], 'STATE': line['State'], 'DISTRICT': line['District'], 'ACTIVE': line['Active'],
                           'CONFIRMED': line['Confirmed'], 'DECEASED': line['Deceased'], 'RECOVERED': line['Recovered'], 'NOTES': line['District_Notes']})
    # print(myList)

with open(covid_report_file, "w") as report:
    fields = ["KEY", "STATE", "DISTRICT", "ACTIVE",
              "CONFIRMED", "RECOVERED", "DECEASED", "NOTES"]
    csv_writer = csv.DictWriter(report, fieldnames=fields)
    csv_writer.writeheader()

    with open(input_file, "r") as input:
        input_obj = csv.DictReader(input)
        for input_line in input_obj:
            for line in myList:
                input_district = input_line['DISTRICT'].lower()
                if((input_district == line['DISTRICT'].lower()) or (input_district == line['STATE'].lower())
                   or (input_district == line['KEY'].lower().split('_')[0]) or (input_district == line['KEY'].lower().split('_')[1])):

                    csv_writer.writerow(line)

csv_file = pd.read_csv(covid_report_file)
csv_file.to_html(report_webpage)
html_file = csv_file.to_html()

openWeb(report_webpage)
