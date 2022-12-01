def F_to_C(temp_F):
    return round((temp_F - 32) * (5 / 9), 2)


import altair as alt
import pandas as pd

source = pd.read_csv("./basic_charts_data/bergen_weather.csv")


alt.Chart(
    source, title="2021-22 Daily High Temperature (C) in Bergen, Norway"
).mark_rect().encode(
    alt.X(
        "date(DATE):N",
        # sort=alt.EncodingSortField(field='TMAX', op='max',order='descending')
    ),
    alt.Y(
        "month(DATE):N",
        # sort=alt.EncodingSortField(field='TMAX', op='mean',order='descending')
    ),
    color=alt.Color("TMAX:Q", scale=alt.Scale(scheme="inferno")),
    tooltip=[
        alt.Tooltip("monthdate(DATE):T", title="Date"),
        alt.Tooltip("TMAX:Q", title="Max Temp"),
    ],
).properties(
    width=550
).save(
    "./basic_charts_html_output/heatmap.html"
)
