import altair as alt
from vega_datasets import data
# from https://github.com/vega/vega-datasets/tree/master/data

source = data.gapminder_health_income()
print(source.head())


# truncate y axis for more spread out representation
scatter_plot_linear = alt.Chart(source).mark_circle().encode(
        alt.X('income:Q', title='Income'),
        alt.Y('health:Q', scale=alt.Scale(zero=False), title='Health'),
        color=alt.value('steelblue'),
        # fillOpacity=alt.value(0.5),
        strokeOpacity=alt.value(1),
        tooltip=['country', 'income', 'health', 'population']
    ).interactive()

# logarithmic scale to spread out countries on lower end of x-scale and encode population into visualization 
scatter_plot_log = alt.Chart(source).mark_circle().encode(
        alt.X('income:Q', scale=alt.Scale(type='log'), title='Income (log)'),
        alt.Y('health:Q', scale=alt.Scale(zero=False), title='Health'),
        size=alt.Size(
            'population:Q', 
            scale=alt.Scale(range=[20,2000])
            ),
        color=alt.Color(
            'population:Q',
            # legend=None, 
            scale=alt.Scale(scheme='tealblues'),
            ),
        # fillOpacity=alt.value(0.5),
        strokeOpacity=alt.value(1),
        tooltip=['country', 'income', 'health', 'population']
    ).interactive()

alt.hconcat(scatter_plot_linear,scatter_plot_log).save('./basic_charts_html_output/scatter.html')
