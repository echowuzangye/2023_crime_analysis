import json
import pandas as pd
import requests
import csv
import numpy as np


API_key = 'rx7BYAXKwqiVZAbceOuSglJxenmh3pr2xh9lztXc'
crime_url = 'https://api.usa.gov/crime/fbi/cde'

agency_query = '/agency/byStateAbbr/'


state_name = ['AL','AK','AS','AZ','AR','CA','CO','CT','DE','DC','FL','GA','GU','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA',
              'MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','MP','OH','OK','OR','PA','PR','RI','SC','SD','TN','TX',
              'UT', 'VT', 'VA', 'VI','WA','WV','WI', 'WY']

# Agency
# collect all Agency info and save them as csv files
# Provides agencies that have provided data to the UCR Program and are displayed on the CDE.
# https://api.usa.gov/crime/fbi/cde/agency/byStateAbbr/NJ?API_KEY=iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv

for state in state_name:
    response = requests.get(crime_url + agency_query +  state + '?API_KEY=' + API_key)
    data = response.json()

    fields = ["ori", "agency_name", "agency_id", "state_abbr", "division_name", "region_name", "region_desc", "county_name", "agency_type_name",
        "nibrs", "nibrs_start_date", "latitude" , "longitude"]
    # Open a new CSV file and write the header row
    with open(f'agency/{state}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(fields)
        # Write each data row to the CSV file
        for row in data:
            writer.writerow([row[field] for field in fields])


## Arrest on national level
#  Provides details of the number of arrests, citations, or summons for an offense. 
# View arrest information on the national level along with federal, state, and local agencies.
            
# https://api.usa.gov/crime/fbi/cde/arrest/national/all?from=1900&to=2023&API_KEY=xxxxxx

response = requests.get(crime_url + '/arrest/national/all?from=1900&to=2023&API_KEY=' + API_key)
data = response.json()
keys = data['keys']
keys.append('data_year')
arrest_data = data['data']
# Open a new CSV file and write the header row
with open('arrest_national.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(keys)
    # Write each data row to the CSV file
    for row in arrest_data:
        writer.writerow([row[key] for key in keys])

## Arrest on regional level
#  Provides details of the number of arrests, citations, or summons for an offense. 
# View arrest information on the regional level along with federal, state, and local agencies.
# https://api.usa.gov/crime/fbi/cde/arrest/state/AK/all?from=1900&to=2023&API_KEY=xxxxxxxx

for state in state_name:
    response = requests.get(crime_url + '/arrest/state/' + state + '/all?from=1900&to=2023&API_KEY=' + API_key)
    data = response.json()
    keys = data['keys']
    keys.append('data_year')
    arrest_data = data['data']

    with open(f'arrest_bystate/{state}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(keys)
        # Write each data row to the CSV file
        for row in arrest_data:
            writer.writerow([row[key] for key in keys])

## Participation - national
# Provides the number of law enforcement agencies that were actively enrolled and submitted data to the UCR Program for a given year. 
# Provides participation details regarding UCR data, NIBRS, hate crime data, and other collections of the UCR Program.
response = requests.get(crime_url + '/participation/national/all/byYearRange?from=1960&to=2023&API_KEY=' + API_key)
data = response.json()
keys = ["data_year",  "population", "total_population"]

# Open a new CSV file and write the header row
with open('participation_national.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(keys)
    # Write each data row to the CSV file
    for row in data:
        writer.writerow([row[key] for key in keys])

## Participation - state
# https://api.usa.gov/crime/fbi/cde/participation/state/AK/all/byYearRange?from=1960&to=2022&API_KEY=iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv
for state in state_name:
    response = requests.get(crime_url + '/participation/state/' + state + '/all/byYearRange?from=1960&to=2022&API_KEY=' + API_key)
    data = response.json()
    keys = ["data_year", "state_id", "state_abbr", "total_population"]
    
    with open(f'participation_bystate/{state}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(keys)
        # Write each data row to the CSV file
        for row in data:
            writer.writerow([row[key] for key in keys])

## Crime estimate
### Provides details regarding reported and converted summary data. 
### Estimated data is available for All Violent Crimes, Homicide, Rape, Robbery, Aggravated Assault, All Property Crimes, Arson, Burglary, Larceny-theft, and Motor Vehicle Theft. Data is available on the national and regional level along with federal, state, and local agencies.
## nation
estimate_keywords=['aggravated-assault', 'violent-crime', 'robbery', 'arson', 'rape-legacy', 'homicide', 'burglary', 'motor-vehicle-theft', 'larceny', 'rape', 'property-crime']
#  https://api.usa.gov/crime/fbi/cde/estimate/national/property-crime?from=1960&to=2022&API_KEY=iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv
for key in estimate_keywords:
    response = requests.get(crime_url + '/estimate/national/' + key + '?from=1960&to=2022&API_KEY=' + API_key)
    data = response.json()['results']
    year = np.arange(1960,2023,1)
    data_keys = data.values()

    with open(f'estimate_national/{key}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(year)
        for row in data_keys:
            writer.writerow([row[str(year)] for year in year])