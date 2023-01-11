import altair as alt
import pandas as pd

bergen_florida_5y = pd.read_csv("./weather_case_study/data/bergen-2018-2022_NEW.csv")
bergen_florida_5y["DATE_YEAR"] = bergen_florida_5y["DATE"].str[:4]
print(bergen_florida_5y.head())

# bergen_2020 = bergen_florida_5y.loc[bergen_florida_5y['DATE_YEAR'] == "2020"].copy()
# print(bergen_2020.head())

input_dropdown = alt.binding_select(options=bergen_florida_5y["DATE_YEAR"].unique(), name="Year")
year_selection = alt.selection_single(fields=['DATE_YEAR'], bind=input_dropdown, init={"DATE_YEAR": "2018"})

brush = alt.selection(type='interval', encodings=['x'])
color = alt.condition(brush, alt.Color('DATE_YEAR:N'), alt.value('lightgray'))

# precipitation bar chart 
precip = (
    alt.Chart(bergen_florida_5y) 
    .mark_bar()
    .encode(
        x=alt.X("month(DATE):T", title="Month", axis=alt.Axis(grid=False)), # date binned by month, 
        y=alt.Y("sum(PRCP):Q", title="Total Precipitation (mm)", stack=True),
        color=color,
    )
    .properties(
        width=800,
        height=100,
        title="Monthly Average Precipitation")
    .add_selection(brush)
    .add_selection(year_selection)
    .transform_filter(year_selection)
)

temp_line = (
    alt.Chart(bergen_florida_5y) 
    .mark_line()
    .encode(
        x=alt.X("monthdate(DATE):T", title="Month", axis=alt.Axis(grid=False)), # date binned by month
        y=alt.Y("TAVG:Q", title="Mean Temperature Range (C)", stack=None),
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
        width=800,
        height=300,
        title="Monthly Average Temperature")
    .transform_filter(year_selection)
    .transform_filter(brush)
)

temp_range = temp_line.mark_bar().encode(
        y=alt.Y("TMIN:Q"),
        y2=alt.Y2("TMAX:Q"),
        # x=alt.X("monthdate(DATE):T"),
        color=alt.Color("TAVG:Q", scale=alt.Scale(scheme="redyellowblue"), sort="descending"),
        opacity=alt.value(0.9),
        size=alt.value(2)
    ).transform_filter(brush)



# combine charts to one view
alt.vconcat(
    temp_range+temp_line,precip
    ).configure_view(strokeWidth=0
    ).show()



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
