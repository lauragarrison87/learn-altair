import altair as alt
from vega_datasets import data
from altair_saver import save


source = data.cars()

plot = alt.Chart(source).mark_tick().encode(x="Horsepower:Q", y="Cylinders:O")

save(
    plot, "plot.png", vega_cli_options=["-s 4"]
)  # scaling factor for higher resolution png file
save(plot, "car-strip.pdf")  # save as pdf instead
