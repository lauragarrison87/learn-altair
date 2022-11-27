# from https://gist.github.com/andfanilo/2e3c7605ec71bce603264ce2fdbf61eb

import altair as alt
import streamlit as st
from vega_datasets import data

chart = None

@st.cache
def get_data():
    return data.gapminder_health_income()

source = get_data()

selection = alt.selection_interval(bind="scales")

chart = alt.Chart(source).mark_circle().encode(
    x=alt.X("income:Q", scale=alt.Scale(type="log")),
    y=alt.Y("health:Q", scale=alt.Scale(zero=False), axis=alt.Axis(minExtent=30)),
    size=alt.Size("population:Q"),
    color=alt.ColorValue("#000")
).properties(
    width=500,
    height=300
).add_selection(selection)

if chart:
    st.altair_chart(chart, use_container_width=True)