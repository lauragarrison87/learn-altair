# Libraries needed 
import requests
import pandas as pd

# Insert your own client ID here
client_id = '06bad647-8ea1-440e-aee1-b17732efcfa6'

# retrieve data from Frost using requests.get()
# Define endpoint and parameters
# elements: https://frost.met.no/elementtable,https://frost.met.no/dataclarifications.html
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN50540',
    'elements': 'max(air_temperature P1D),min(air_temperature P1D),mean(air_temperature P1D),surface_snow_thickness,sum(precipitation_amount P1D),mean(wind_speed P1D)',
    'referencetime': '2022-11-01/2022-11-06',
    'timeoffsets': 'default',
}
# Issue an HTTP GET request
r = requests.get(endpoint, parameters, auth=(client_id,''))
# Extract JSON data
json = r.json()

# Check if the request worked, print out any errors
if r.status_code == 200:
    data = json['data']
    print('Data retrieved from frost.met.no!')
else:
    print('Error! Returned status code %s' % r.status_code)
    print('Message: %s' % json['error']['message'])
    print('Reason: %s' % json['error']['reason'])

# This will return a Dataframe with all of the observations in a table format
df = pd.DataFrame()
for i in range(len(data)):
    row = pd.DataFrame(data[i]['observations'])
    row['referenceTime'] = data[i]['referenceTime']
    row['sourceId'] = data[i]['sourceId']
    df = df.append(row)

df = df.reset_index()
# These additional columns will be kept
columns = ['sourceId','referenceTime','elementId','value','unit','timeOffset']
df2 = df[columns].copy()

# Convert the time value to something Python understands
df2['referenceTime'] = pd.to_datetime(df2['referenceTime'])

df2.to_csv('data/original_data.csv')


pivoted = df2.pivot(index=None, columns='elementId', values='value')

print(df2.head())
print(pivoted.head())

merged = df2.merge(pivoted, how='inner', left_on=None, right_on=None, left_index=True, right_index=True)
keep_columns = ['sourceId','referenceTime','mean(air_temperature P1D)','mean(wind_speed P1D)','sum(precipitation_amount P1D)','unit','timeOffset']
merged2 = merged[keep_columns].copy()
print(merged2.head())

#merged2.to_csv('bergen_values_nov.csv')
