import altair as alt
import pandas as pd

# get data
source = pd.read_csv("./basic_charts_data/gapminder_ddf_1800_2014.csv")
source["Year"] = pd.to_datetime(source["Year"], format="%Y")

alt.data_transformers.disable_max_rows()  # enable altair to load data >5000 rows

brush = alt.selection(type="interval")

# show for all years
global_pop_all = (
    alt.Chart(source)
    .mark_line()
    .encode(
        alt.X(
            "Year:T",
            timeUnit="year",
            # scale=alt.Scale(domain=x_domain),
            title="Year",
        ),
        alt.Y(
            "sum(Population):Q",
            # scale=alt.Scale(domain=y_domain)
        ),
        color="Region",
    )
    .add_selection(brush)
    .properties(width=500, height=400, title="Global Population by Region: 1800-2014")
)  # .interactive()
# .facet('Region:N',columns = 2)

global_pop_all.configure_title(fontSize=20, anchor="start")

# compare population growth in different regions of world over time
# x_domain = ["1900", "1960"]
# y_domain = [0, 1800000000]

global_pop = (
    alt.Chart(source)
    .mark_line(point=alt.OverlayMarkDef(), clip=True)
    .encode(
        alt.X(
            "Year:T",
            timeUnit="year",
            # scale=alt.Scale(domain=x_domain),
            title="Year",
        ),
        alt.Y(
            "sum(Population):Q",
            # scale=alt.Scale(domain=y_domain)
        ),
        color="Region",
    )
    .transform_filter(brush)
    .properties(width=500, height=400, title="Global Population by Region: Detail")
)  # .interactive()
# .facet('Region:N',columns = 2)

global_pop.configure_title(fontSize=20, anchor="start")


alt.vconcat(global_pop_all, global_pop).save("./basic_charts_html_output/line.html")
