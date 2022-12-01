import altair as alt
import pandas as pd

# Read in and prep data
source = pd.read_json("basic_charts_data/penguins.json")
source_cropped = source[["Species", "Island"]]

island_species_count = (
    source_cropped.groupby(["Island", "Species"])
    .size()
    .reset_index(name="Species_count")
)

species_count = source_cropped.groupby(["Island"]).count().reset_index()
merged = pd.merge(
    island_species_count, species_count, on="Island", suffixes=["", "_sum"]
)

merged["Island_Species_frac"] = round(
    merged["Species_count"] / merged["Species_sum"], 2
)

# data prep for coxcomb plot
species_count_all = (
    source_cropped.groupby(["Species"]).size().reset_index(name="Species_count")
)
species_count_all["Species_frac"] = (
    species_count_all["Species_count"] / species_count_all["Species_count"].sum()
)
print(species_count_all)

# Pie chart radial variant
pie = (
    alt.Chart(merged)
    .mark_arc()
    .encode(
        theta=alt.Theta("Island_Species_frac:Q"),
        color=alt.Color("Species:N"),
        tooltip=[
            alt.Tooltip("Species:N", title="Species"),
            alt.Tooltip(
                "Island_Species_frac:Q", title="Fraction penguin species on island"
            ),
        ],
    )
    .properties(
        width=150,
        height=150,
    )
    .facet("Island:N", columns=3)
    .configure_view(strokeWidth=0)
    .save("./basic_charts_html_output/pie.html")
)

# Donut chart radial variant
donut = (
    alt.Chart(merged)
    .mark_arc(innerRadius=50)
    .encode(
        theta=alt.Theta("Island_Species_frac:Q"),
        color=alt.Color("Species:N"),
        tooltip=[
            alt.Tooltip("Species:N", title="Species"),
            alt.Tooltip(
                "Island_Species_frac:Q", title="Fraction penguin species on island"
            ),
        ],
    )
    .properties(
        width=150,
        height=150,
    )
    .facet("Island:N", columns=3)
    .configure_view(strokeWidth=0)
    .save("./basic_charts_html_output/donut.html")
)


# Coxcomb chart radial variant
coxcomb = alt.Chart(species_count_all).encode(
    theta=alt.Theta("Species_frac:Q", stack=True),
    radius=alt.Radius(
        "Species_frac:Q", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)
    ),
    color="Species:N",
)

c1 = (
    coxcomb.mark_arc(innerRadius=20, stroke="#fff")
    .configure_view(strokeWidth=0)
    .save("./basic_charts_html_output/coxcomb.html")
)

# bar version of coxcomb for comparison
bar_version = (
    alt.Chart(species_count_all)
    .mark_bar()
    .encode(alt.Y("Species_count:Q", stack="normalize"), color="Species:N")
    .save("./basic_charts_html_output/coxcomb_bar_version.html")
)
