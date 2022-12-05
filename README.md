# Visualization in your development process 

Content for 2022 ICTP Collaborative programming school

## Vega-Altair Basics 

Code for some of the basic visualization idioms in Vega-Altair available in [`./basic_charts`](./basic_charts/). 

The local data inputs for these charts can be found in [`./basic_charts_data`](./basic_charts_data/). 

Run these files from the root directory so that the local data source is findable. For example: 

    python3 ./basic_charts/bar.py

Each of these files saves a chart in `html` format, which outputs to [`basic_charts_html_output`](./basic_charts_html_output/).

## Weather Exploration

For a practical example of using visualization to help answer a question, we have a dataset of the daily weather summary from Bergen, Norway, from 2018-22, downloaded from [NOAA](https://www.ncdc.noaa.gov/cdo-web/datasets). 

Local data source resides in [`./weather_case_study/data`](./weather_case_study/data). Run the python files from `./weather_case_study`, for example:

    python3 ./weather_case_study/bergen_weather.py

The python files write charts out in `html` format to [`./weather_case_study/output`](./weather_case_study/output). The files in this directory are numbered in order of how I explored the data to answer the question, *Has it really rained that much in Bergen this year?*


## Animation

This section explores how to incorporate animation into Vega-Altair charts. At this time (Dec 2022), this charting library does not natively support animation, so we have to add other tools to make this work. 

1. GapMinder Data: Health vs. Wealth over time 
2. Wind flux (adapted from [Wind Vector Map](https://altair-viz.github.io/gallery/wind_vector_map.html))