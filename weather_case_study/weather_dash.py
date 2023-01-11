import altair as alt
import pandas as pd

bergen_florida_5y = pd.read_csv("./weather_case_study/data/bergen-2018-2022_NEW.csv")
bergen_florida_5y["DATE_YEAR"] = bergen_florida_5y["DATE"].str[:4]

print(bergen_florida_5y.head())


# custom color scale
# scale = alt.Scale(domain=['sun', 'fog', 'drizzle', 'rain', 'snow'],
#                   range=['#e7ba52', '#c7c7c7', '#aec7e8', '#1f77b4', '#9467bd'])

# select years in chart
select_year = alt.selection_multi(fields=["DATE_YEAR"])
color = alt.condition(select_year, 
    alt.Color("DATE_YEAR:N", legend=None), 
    alt.value("lightgray"))

# selector 
year_selector = (
    alt.Chart()
    .mark_square()
    .encode(
        alt.X("year(DATE):N", axis=alt.Axis(orient="top"), title=None),
        color = color
    )
    .properties(title="Select Year:", width = 150)
    .add_selection(select_year)
)

# precipitation bar chart 
precip = (
    alt.Chart() 
    .mark_bar()
    .encode(
        alt.X("month(DATE):T", title="Month"), # date binned by month
        alt.Y("sum(PRCP):Q", title="Total Precipitation (mm)"), # monthly sum of precipitation
        color=alt.Color("DATE_YEAR:N"), # stacked bar chart
    )
    .properties(width=600,height=200,title="Monthly Rainfall")
    .transform_filter(select_year)
).interactive()


# temp monthly line chart 
temp = (
    alt.Chart() 
    .mark_line()
    .encode(
        alt.X("month(DATE):T", title="Month"), # date binned by month
        alt.Y("mean(TAVG):Q", title="Mean Temperature Range (C)", stack=None), # monthly sum of precipitation
        color=alt.Color("DATE_YEAR:N"), # stacked bar chart,
        tooltip="yearmonth(DATE):T"
    )
    .properties(width=600,height=200,title="Monthly Average Temperature Range")
    .transform_filter(select_year)
).interactive()

# temp daily line chart 
temp_daily = (
    alt.Chart() 
    .mark_circle(opacity=0.4)
    .encode(
        alt.X("monthdate(DATE):T"), # date binned by month
        alt.Y("TMIN:Q", stack=None), # monthly sum of precipitation
        color=alt.Color("DATE_YEAR:N"), # stacked bar chart
        tooltip=["DATE:T"]
    )
    .transform_calculate(
        temp_range="datum.TMAX - datum.TMIN"
    )
    .properties(width=600,height=200)
    .transform_filter(select_year)
).interactive()

# combine charts to one view
alt.vconcat(
    year_selector,temp,precip, data=bergen_florida_5y
    ).configure_view(strokeWidth=0
    ).show()

# temperature dumbbell chart 