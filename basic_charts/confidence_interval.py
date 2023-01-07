import altair as alt
import pandas as pd

source = pd.read_csv("./data/bergen_weather.csv")

ci = (
    alt.Chart(source)
    .mark_errorband(extent="ci", opacity=0.2)
    .encode(
        alt.X("month(DATE)"),
        alt.Y("PRCP:Q", title="Precip"),
    )
    .properties(title="Average Monthly Rain in 2022 with 95% CI")
)

line = ci.mark_line().encode(alt.Y("average(PRCP):Q"))

(line + ci).show()
# (line + ci).save("./html_output/confidence_interval.html")
