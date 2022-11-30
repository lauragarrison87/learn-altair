import altair as alt
from vega_datasets import data
import pandas as pd

# get data 
penguins_data = pd.read_json('basic_charts_data/penguins.json')

# clean data 
penguins_data = penguins_data.dropna()
penguins_data = penguins_data[(penguins_data.Sex !='.')]

# how is gender balanced across penguin species?
penguin_species_bar = alt.Chart(penguins_data).mark_bar().encode(
    alt.X('Species:N',sort='y'),
    y='count(Species)',
    color = 'Sex',
    # order=alt.Order(
    #   # Sort the segments of the bars by this field
    #   'Species','Sex',
    #   sort='ascending'
    # )
).properties(
    title='Penguin Gender\nby Species'
)

penguin_species_bar.configure_title(
    fontSize=20,
    anchor='start'
).save('./basic_charts_html_output/stacked_bar.html')


# normalized version of chart 
penguin_species_bar = alt.Chart(penguins_data).mark_bar().encode(
    alt.X('Species:N'),
    alt.Y('count(Species)', stack='normalize'),
    color = 'Sex',
    # order=alt.Order(
    #   # Sort the segments of the bars by this field
    #   'Sex',
    #   sort='ascending'
    # )
).properties(
    title='Penguin Gender\nby Species'
)

penguin_species_bar.configure_title(
    fontSize=20,
    anchor='start'
).save('./basic_charts_html_output/normalized_stacked_bar.html')
    



