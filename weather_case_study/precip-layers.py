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
        width=800, # use this if you want the width to be inherited from what you specify in your <div> for the vis
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

(precip+tick).add_selection(year_selection).add_selection(brush).show()
