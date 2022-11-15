import altair as alt
from vega_datasets import (
    data,
)  # from https://github.com/vega/vega-datasets/tree/master/data

source = data.gapminder_health_income()
print(source.head())

# plot health against income for all countries
scatter_plot_linear = (
    alt.Chart(source)
    .mark_point()
    .encode(
        alt.X("income:Q"),
        alt.Y(
            "health:Q", scale=alt.Scale(zero=False)
        ),  # what happens if this is set to true?
    )
)

scatter_plot_log = (
    alt.Chart(source)
    .mark_circle()
    .encode(
        alt.X("income:Q", scale=alt.Scale(type="log")),
        alt.Y("health:Q", scale=alt.Scale(zero=False)),
    )
)

scatter_plot_linear.show()  # to display in altair viewer (must be installed separately)
scatter_plot_log.show()  # log spreads things out a bit more

# chart.save('basic-chart.html')
