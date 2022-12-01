# code from: https://altair-viz.github.io/gallery/streamgraph.html

import altair as alt
import pandas as pd

source = pd.read_json(
    "https://raw.githubusercontent.com/vega/vega-datasets/master/data/unemployment-across-industries.json"
)
print(source.head())

gapminder_src = pd.read_csv("./basic_charts_data/gapminder_ddf.csv")

# STACKED AREA
stacked_area = (
    alt.Chart(source)
    .mark_area()
    .encode(
        alt.X(
            "yearmonth(date):T", axis=alt.Axis(format="%Y", domain=False, tickSize=0)
        ),
        alt.Y("sum(count):Q"),
        alt.Color("series:N", scale=alt.Scale(scheme="category20b")),
    )
    .properties(title="US Unemployment Across Sectors: Stacked Area Chart")
    .interactive()
)


stacked_area.configure_title(fontSize=20, anchor="start")


# STREAMGRAPH
streamgraph = (
    alt.Chart(source)
    .mark_area()
    .encode(
        alt.X(
            "yearmonth(date):T", axis=alt.Axis(format="%Y", domain=False, tickSize=0)
        ),
        alt.Y("sum(count):Q", stack="center", axis=None),
        alt.Color("series:N", scale=alt.Scale(scheme="category20b")),
    )
    .properties(title="US Unemployment Across Sectors: Streamgraph")
    .interactive()
)


streamgraph.configure_title(fontSize=20, anchor="start")

alt.vconcat(stacked_area, streamgraph).save(
    "./basic_charts_html_output/area_stream.html"
)
