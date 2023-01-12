import altair as alt
import pandas as pd

bergen_florida_5y = pd.read_csv("./weather_case_study/data/bergen-2018-2022_NEW.csv")
bergen_florida_5y["DATE_YEAR"] = bergen_florida_5y["DATE"].str[:4]
print(bergen_florida_5y.head())

# interactive stuff 
input_dropdown = alt.binding_select(options=bergen_florida_5y["DATE_YEAR"].unique(), name="Year")
year_selection = alt.selection_single(fields=['DATE_YEAR'], bind=input_dropdown, init={"DATE_YEAR": "2018"})

brush = alt.selection(type='interval', encodings=['x']) # click and drag to select interval of interest
# brush = alt.selection_single(on="mouseover", encodings=['x']) # use mouseover instead of click
color = alt.condition(brush, alt.Color('DATE_YEAR:N', legend=alt.Legend(title="Year")), alt.value('lightgray'))

# precipitation bar chart
precip = (
    alt.Chart(bergen_florida_5y) 
    .mark_bar()
    .encode(
        x=alt.X("month(DATE):O", title="Month", axis=alt.Axis(grid=False)), # date binned by month, 
        y=alt.Y("mean(PRCP):Q", title="Precipitation (mm)", stack=True),
        color=color,
        tooltip=[
            alt.Tooltip("yearmonth(DATE):T", title="Date"), 
            alt.Tooltip("max(PRCP):Q", title="Precip Daily Max"),
            alt.Tooltip("mean(PRCP):Q", title="Precip Avg")
            ]
    )
    .properties(
        width="container", # use this if you want the width to be inherited from what you specify in your <div> for the vis
        height=200,
        title="Monthly Precipitation (Maximum Daily and Monthly Average)")
    # .add_selection(brush)
    # .add_selection(year_selection)
    .transform_filter(year_selection)
)

tick = precip.mark_tick(
    thickness=2,
    size=40 * 0.9,  # controls width of tick.
).encode(
    x=alt.X("month(DATE):O"),
    y=alt.Y("max(PRCP):Q"),
    color=alt.value("steelblue")
)

# temperature charts -- layer on top of eachother in final vis
temp_line = (
    alt.Chart(bergen_florida_5y) 
    .mark_line()
    .encode(
        x=alt.X("monthdate(DATE):T", title="Month", axis=alt.Axis(grid=False)), # date binned by month
        y=alt.Y("TAVG:Q", title="Mean Temperature Range (°C)", stack=None),
        color=alt.value("black"),
        opacity=alt.value(0.4),
        tooltip=[
            alt.Tooltip("yearmonth(DATE):T", title="Date"), 
            alt.Tooltip("TMAX", title="Max Temp"), 
            alt.Tooltip("TAVG", title="Avg Temp"), 
            alt.Tooltip("TMIN", title="Min Temp")
            ]
    )
    .properties(
        width="container",
        height=300,
        title="Monthly Average Temperature")
    .transform_filter(year_selection)
    # .transform_filter(brush)
)

temp_range = temp_line.mark_bar().encode(
        y=alt.Y("TMIN:Q"),
        y2=alt.Y2("TMAX:Q"),
        # x=alt.X("monthdate(DATE):T"),
        color=alt.Color("TAVG:Q", scale=alt.Scale(scheme="redyellowblue"), sort="descending", legend=alt.Legend(title="Avg Temp (°C)")),
        opacity=alt.value(0.9),
        size=alt.value(2)
    ).transform_filter(brush)



# create my dashboard vis
# alt.vconcat(
#     temp_range+temp_line,precip
#     ).configure_view(strokeWidth=0
#     ).save("./weather_case_study/output/weather_dash2.json") # output to json to embed in weather-dash.html
alt.vconcat(
    temp_range+temp_line,precip+tick.add_selection(year_selection).add_selection(brush)
    ).configure_view(strokeWidth=0
    ).save("./weather_case_study/output/weather_dash2.json") # output to json to embed in weather-dash.html


####### UNUSED

# temp_freeze = (
#     temp_line
#     .mark_circle()
#     .encode(
#         y=alt.Y("TAVG:Q", title="Mean Temperature Range (C)", stack=None),
#         color=alt.condition(alt.datum.TMIN > 0, alt.value('red'), alt.value('blue')),
#         tooltip="yearmonth(DATE):T"
#     )
# )
