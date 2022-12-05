import altair as alt
import pandas as pd

# but now I want to compare this over 5 years
bergen_florida_5y = pd.read_csv("./weather_case_study/data/bergen_weather_2018_22.csv")
print(bergen_florida_5y.head())

highlight = alt.selection_single(on="mouseover")

base = (
    alt.Chart(bergen_florida_5y)
    .mark_line()
    .encode(
        alt.X("month(DATE):T"),
        alt.Y("average(PRCP)"),
        strokeWidth=alt.value(3),
        color=alt.condition(highlight, "year(DATE):N", alt.value("lightgray")),
    )
    .add_selection(highlight)
    .properties(title="Average Monthly Rain in Bergen 2018-22", width=500, height=500)
)
base.save("./weather_case_study/output/6_precip_month_2018_22.html")

# this looks cool, but is very cluttered. What if we just plotted CI instead?
# add a bootstrapped 95% confidence interval band
band = (
    base.mark_errorband(extent="ci", opacity=0.2).encode(
        alt.Y("PRCP:Q", title="Precip"),
        # color=alt.condition(highlight, "year(DATE):N", alt.value("lightgray")),
        alt.Color("year(DATE):N"),
    )
    # .add_selection(highlight)
)


(band + base).save("./weather_case_study/output/7_precip_month_2018_22_band.html")
