import altair as alt
import pandas as pd

# read in data
source = "./weather_case_study/data/bergen_weather_2022.csv"
data = pd.read_csv(source)

# I only want to look at the Bergen Florida weather station
bergen_florida = data.loc[data["STATION"] == "NO000050540"]
bergen_florida["PRCP"] = bergen_florida["PRCP"].dropna()
print(len(bergen_florida))
print(bergen_florida.head())

# how is the rain distributed throughout the year? When did these huge rain days happen? When are the so-called 200 "dry" days we saw in the binned plot happening?
precip_time = (
    alt.Chart(bergen_florida)
    .mark_line()
    .encode(alt.X("DATE:T"), alt.Y("PRCP:Q"), tooltip=["DATE:T", "PRCP"])
    .properties(title="Daily Rain in Bergen in 2022", width=1000, height=500)
)
precip_time.save("./weather_case_study/output/precip_time.html")

# what is the distribution of high-low rain days in a different way
precip = (
    alt.Chart(bergen_florida)
    .mark_bar()
    .encode(alt.X("PRCP:Q"), alt.Y("count(PRCP)"))
    .properties(title="Count of Rain Amounts in Bergen in 2022")
)
precip.save("./weather_case_study/output/precip_raw.html")

# maybe I want to bin this data (quantitative data harder)
precip_binned = (
    alt.Chart(bergen_florida)
    .mark_bar()
    .encode(alt.X("PRCP", bin=True), alt.Y("count(PRCP)"))
    .properties(title="Count of Rain Amounts in Bergen in 2022")
)  # .transform_bin("binned_precip", "PRCP", bin=alt.Bin(maxbins=10))
precip_binned.save("./weather_case_study/output/precip_binned.html")

# how does the rain amount break down per month? Are there really dry/really rainy months?
precip_time_month = (
    alt.Chart(bergen_florida)
    .mark_line(color="black")
    .encode(
        alt.X("yearmonth(DATE):T"),
        alt.Y("average(PRCP)"),
        tooltip=[
            alt.Tooltip("average(PRCP):Q", format=",.2f", title="Avg month precip")
        ],
    )
    .properties(title="Average Monthly Rain in Bergen in 2022", width=800, height=500)
)
precip_time_month.save("./weather_case_study/output/precip_time_month.html")

# so this gives the average, but what if I want to show the full range here?
points = precip_time_month.mark_circle(opacity=0.7).encode(
    alt.X("DATE:T"),
    alt.Y("PRCP"),
    alt.Color("month(DATE):N", scale=alt.Scale(scheme="tableau20")),
    tooltip=["DATE:T", "PRCP"],
)

(precip_time_month + points).save(
    "./weather_case_study/output/precip_time_month_avg_ind.html"
)
