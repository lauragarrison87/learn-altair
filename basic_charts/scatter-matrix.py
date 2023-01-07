import altair as alt
import pandas as pd

# Read in and prep data
source = pd.read_json("./data/penguins.json")
print(source.head())

# adapt from the cars dataset
alt.Chart(source).mark_circle().encode(
    alt.X(alt.repeat("column"), type="quantitative"),
    alt.Y(alt.repeat("row"), type="quantitative"),
    color="Species:N",
).properties(width=150, height=150).repeat(
    row=["Beak Length (mm)", "Beak Depth (mm)", "Flipper Length (mm)", "Body Mass (g)"],
    column=[
        "Beak Length (mm)",
        "Beak Depth (mm)",
        "Flipper Length (mm)",
        "Body Mass (g)",
    ],
).interactive().show()#.save("./html_output/scatter-matrix.html")
