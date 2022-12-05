import altair as alt
import pandas as pd

# read in data
data = pd.read_csv("./weather_case_study/data/bergen_weather_2018_22.csv")

# only look at weather data from this year (2022)
data["DATE"] = pd.to_datetime(data["DATE"], format="%Y-%m-%d")
bergen_2022 = data.loc[(data["DATE"] >= "2022-01-01")]
print(bergen_2022.head())

# how is the rain distributed throughout the year? When did these huge rain days happen? When are the so-called 200 "dry" days we saw in the binned plot happening?
precip_time = (
    alt.Chart(bergen_2022)
    .mark_line()
    .encode(alt.X("DATE:T"), alt.Y("PRCP:Q"), tooltip=["DATE:T", "PRCP:Q"])
    .properties(title="Daily Rain in Bergen (2022)", width=1000, height=500)
)
precip_time.save("./weather_case_study/output/1_precip_time.html")

# what is the distribution of high-low rain days in a different way
precip = (
    alt.Chart(bergen_2022)
    .mark_bar()
    .encode(alt.X("PRCP:Q"), alt.Y("count(PRCP)"))
    .properties(title="Count of Rain Amounts in Bergen in 2022")
)
precip.save("./weather_case_study/output/2_precip_amt_freq.html")

# maybe I want to bin this data (quantitative data harder)
precip_binned = (
    alt.Chart(bergen_2022)
    .mark_bar()
    .encode(alt.X("PRCP:Q", bin=True), alt.Y("count(PRCP)"))
    .properties(title="Count of Rain Amounts in Bergen in 2022")
)  # .transform_bin("binned_precip", "PRCP", bin=alt.Bin(maxbins=10))
precip_binned.save("./weather_case_study/output/3_precip_freq_binned.html")

# how does the rain amount break down per month?
# Are there really dry/really rainy months?
precip_time_month = (
    alt.Chart(bergen_2022)
    .mark_line(color="black")
    .encode(
        alt.X("yearmonth(DATE):T"),
        alt.Y("average(PRCP):Q"),
        tooltip=[
            alt.Tooltip("average(PRCP):Q", format=",.2f", title="Avg month precip")
        ],
    )
    .properties(title="Average Monthly Rain in Bergen in 2022", width=800, height=500)
)
precip_time_month.save("./weather_case_study/output/4_precip_time_month.html")

# so this gives the average, but what if I want to show the full range here?
line = precip_time_month.mark_trail(opacity=0.8).encode(
    alt.X("DATE:T"),
    alt.Y("PRCP:Q"),
    alt.Size("average(PRCP)"),
    alt.Color("month(DATE):N", scale=alt.Scale(scheme="tableau20")),
    tooltip=["DATE:T", "PRCP"],
)

(precip_time_month + line).save(
    "./weather_case_study/output/5_precip_time_month_avg_ind.html"
)
