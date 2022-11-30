import altair as alt
from vega_datasets import data

cars = data.cars()

alt.Chart(cars).mark_area(opacity=0.3).encode(
    x='Year:T',
    color='Origin',
    y='ci0(Miles_per_Gallon)',
    y2='ci1(Miles_per_Gallon)'
).save('./basic_charts_html_output/confidence_interval.html')