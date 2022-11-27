import altair as alt
from vega_datasets import data
import pandas as pd

# get data 
penguins_data = pd.read_json('data/penguins.json')

# clean data 
penguins_data = penguins_data.dropna()
penguins_data = penguins_data[(penguins_data.Sex !='.')]


# how is gender balanced across penguin species?
penguin_species_bar = alt.Chart(penguins_data).mark_bar().encode(
    x ='Species:N',
    y='count()',
    color = 'Sex'
).properties(
    title='Penguin Gender\nby Species'
)

penguin_species_bar.configure_title(
    fontSize=20,
    anchor='start'
).save('./html_charts/stacked_bar.html')
    



