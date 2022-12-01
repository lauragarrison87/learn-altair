import altair as alt
import pandas as pd

# but now I want to compare this over 5 years
bergen_florida_5y = pd.read_csv("./weather_case_study/data/bergen_weather_2018_22.csv")

precip_time_month = (
    alt.Chart(bergen_florida_5y)
    .mark_line()
    .encode(
        alt.X("month(DATE):T"),
        alt.Y("average(PRCP)"),
        color="year(DATE):N",
        tooltip=[
            alt.Tooltip("average(PRCP):Q", format=",.2f", title="Avg month precip")
        ],
    )
    .properties(title="Average Monthly Rain in Bergen 2018-22", width=500, height=500)
)
precip_time_month.save("./weather_case_study/output/precip_time_month_2018_22.html")

# let's see how the individual values distribute within each month
points = precip_time_month.mark_circle(opacity=0.3).encode(
    alt.Y("PRCP:Q"),
    tooltip=["DATE:T", "PRCP"],
    color="year(DATE):N",
)

(points + precip_time_month).save(
    "./weather_case_study/output/precip_time_month_2018_22_avg_ind.html"
)

# this looks cool, but is very cluttered. What if we just plotted CI instead?
# add a bootstrapped 95% confidence interval band
band = precip_time_month.mark_errorband(extent="ci", opacity=0.2).encode(
    alt.Y("PRCP:Q", title="Precip"),
    alt.Color("year(DATE):N"),
)
(band + precip_time_month).save(
    "./weather_case_study/output/precip_time_month_2018_22_band.html"
)
