# from http://vega.github.io/vega-lite/tutorials/explore.html

import pandas as pd
import altair as alt 

# load data
csv_file = r'C:\Users\laura\Documents\visual-dev\learn-altair\data\bergen-weather.csv'
df = pd.read_csv(csv_file)

# format data
cleaned_df = df.drop(['STATION', 'NAME'], axis=1)
cleaned_df.columns = ['date', 'precipitation', 'snow_depth', 'temp_avg', 'temp_max', 'temp_min']
print(cleaned_df.head()) # check

# explore data (visually!)
# Q1: what does precipitation look like? let's just plot the data straight-out first
precip_chart = alt.Chart(cleaned_df).mark_tick().encode(
    x='precipitation',
)
#precip_chart.show()
precip_chart.save('precip_chart.html')

# continuous variables like this make patterns harder to see, so we can bin. By binning the data, we can see that there are a lot more days with low rain than days with high amounts of rain
precip_chart_binned = alt.Chart(cleaned_df).mark_bar().encode(
    alt.X('precipitation', bin=True),
    y='count()'
)
#precip_chart_binned.show() 
precip_chart_binned.save('precip_chart_binned.html') 

# how does precipitation in Bergen change throughout the year? 
precip_chart_monthly = alt.Chart(cleaned_df).mark_line().encode(
    # alt.X('month(date)', type='temporal'), # precipitation per month in dataset
    alt.X('yearmonth(date)', type='temporal'), # aggregate on year and month to see seasonal trends
    alt.Y('average(precipitation)')   
)
precip_chart_monthly.save('precip_chart_monthly.html')