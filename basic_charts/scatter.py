import altair as alt
from vega_datasets import data
# from https://github.com/vega/vega-datasets/tree/master/data

source = data.gapminder_health_income()
print(source.head())

# plot health against income for all countries
scatter_plot_linear_zero = alt.Chart(source).mark_circle().encode(
        alt.X("income:Q"),
        alt.Y("health:Q"),
    )

# truncate y axis for more spread out representation
scatter_plot_linear = alt.Chart(source).mark_circle().encode(
        alt.X("income:Q"),
        alt.Y("health:Q", scale=alt.Scale(zero=False)),
    ).interactive()

# logarithmic scale to spread out poorer countries and encode population into visualization 
scatter_plot_log = alt.Chart(source).mark_circle().encode(
        alt.X("income:Q", scale=alt.Scale(type="log"), title='Income'),
        alt.Y("health:Q", scale=alt.Scale(zero=False), title='Health'),
        # size='population:Q'
    ).interactive()

alt.vconcat(
    # scatter_plot_linear_zero, 
    scatter_plot_linear.encode(color='population:O'), 
    scatter_plot_log.encode(size='population:Q', color='population:Q')
    ).save("scatter-charts.html")
