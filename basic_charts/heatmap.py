def F_to_C(temp_F):
    return round((temp_F - 32) * (5 / 9), 2)


import altair as alt
import pandas as pd

source = pd.read_csv("./data/bergen_weather.csv")


heatmap = alt.Chart(
    source, title="2021-22 Daily High Temperature (C) in Bergen, Norway"
).mark_rect().encode(
    alt.X(
        "date(DATE):N",
    ),
    alt.Y(
        "month(DATE):N",
    ),
    color=alt.Color("TMAX:Q", scale=alt.Scale(scheme="inferno")),
    tooltip=[
        alt.Tooltip("monthdate(DATE):T", title="Date"),
        alt.Tooltip("TMAX:Q", title="Max Temp"),
    ],
).properties(
    width=550
)
heatmap.show()

#heatmap.save("./html_output/heatmap.html")
