def F_to_C(temp_F):
    return round((temp_F-32)* (5/9),2)


import altair as alt
import pandas as pd


source = pd.read_csv('./basic_charts_data/bergen-weather.csv')

# convert temp rows from F to C
for column in source[['TAVG', 'TMAX', 'TMIN']]:
    # Select column contents by column name using [] operator
    source[column] = source[column].apply(F_to_C)

print(source.head())


alt.Chart(
    source,
    title="2021-22 Daily High Temperature (C) in Bergen, Norway"
).mark_rect().encode(
    x='date(DATE):O',
    y='month(DATE):O',
    color=alt.Color('TMAX:Q', scale=alt.Scale(scheme="inferno")),
    tooltip=[
        alt.Tooltip('monthdate(DATE):T', title='Date'),
        alt.Tooltip('TMAX:Q', title='Max Temp')
    ]
).properties(width=550).save('./basic_charts_html_output/heatmap.html')