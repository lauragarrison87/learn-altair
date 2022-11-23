import altair as alt
from vega_datasets import data
import pandas as pd

penguins_data = pd.read_json('data/penguins.json')
print(penguins_data.head())

brush = alt.selection(type='interval')

penguin_beak_mass = alt.Chart(penguins_data).mark_circle().encode(
    alt.X('Beak Depth (mm):Q', 
        scale=alt.Scale(zero=False)), #https://altair-viz.github.io/user_guide/customization.html?highlight=custom%20range%20axis
    alt.Y('Body Mass (g):Q', 
        scale=alt.Scale(zero=False)),
    color = alt.Color('Species', legend=alt.Legend(orient="right"))
).add_selection(
    brush
)

# how many of each species of penguin are there?
penguin_species = alt.Chart(penguins_data).mark_bar().encode(
    y ='Species:N',
    x = 'count()',
    color = 'Species'
).properties(
    title='Number of Penguins by Species'
).transform_filter(
    brush
)

penguin_species.configure_title(
    fontSize=20,
    anchor='start'
)#.save('penguin_species_histogram.html')


alt.vconcat(penguin_beak_mass, penguin_species).show()
