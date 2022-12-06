import pandas as pd
import altair as alt
import streamlit as st
import numpy as np
import time

n = 100  # how many time steps


@st.cache  # performance optimization for data load (see https://docs.streamlit.io/library/advanced-features/caching)
def get_data(mydata):
    df = pd.read_csv(mydata)

    df["timestep"] = 0  # create new column for timestep in dataframe

    frames = [df]

    for t in range(1, n):
        df = df.copy()
        df["timestep"] = t
        frames.append(df)

    # combine individ dfs to one huge dataframe
    df_times = pd.concat(frames)

    df_dynamic = df_times

    a_dir = 50
    a_speed = 3
    w = 2 * np.pi / n

    df_dynamic.loc[:, "dir"] += a_dir * np.sin(df_dynamic.loc[:, "timestep"] * w)
    df_dynamic.loc[:, "speed"] += a_speed * np.sin(
        df_dynamic.loc[:, "timestep"] * 2 * w
    )
    df_dynamic.loc[:, "speed"] += a_speed  # keep speed from being below 0
    print(df_dynamic.head())

    return df_dynamic


# from https://altair-viz.github.io/gallery/wind_vector_map.html example on Vega-Altair documentation site
source = get_data("./animation/data/wind.csv")
print(source.describe())

# build the Altair chart
def animate(source):
    chart = (
        alt.Chart(source)
        .mark_point(shape="wedge", filled=True)
        .encode(
            latitude="latitude",
            longitude="longitude",
            color=alt.Color(
                # use cyclical color scheme to highlight cyclical pattern in my data (wind dir is 360 deg possible directions)
                "dir",
                scale=alt.Scale(domain=[0, 360], scheme="sinebow"),
                legend=None,
            ),
            angle=alt.Angle("dir", scale=alt.Scale(domain=[0, 360], range=[180, 540])),
            size=alt.Size("speed", scale=alt.Scale(rangeMax=500)),
        )
        .project("equalEarth")
    )
    return chart


def single_timestep(i):
    global wind_plot
    slider_value = slider_wind.slider(
        "Choose a timestep",
        min_value=0,
        max_value=n,
        value=i,
        label_visibility="collapsed",
    )
    step_df = source.loc[source["timestep"] == slider_value]
    chart = animate(step_df)
    wind_plot = wind_plot.altair_chart(chart)


# set up streamlit interface
wind_plot = st.altair_chart(animate(source.loc[source["timestep"] == 0]))
start_btn = st.button("Start")  # init button
slider_wind = st.empty()  # init slider


slider_value = slider_wind.slider(
    "Choose a timestep",
    min_value=0,
    max_value=n,
    value=0,
    key="slider-start-val",
    label_visibility="collapsed",
)

single_timestep(slider_value)


# animation triggered if start button clicked
if start_btn:
    for i in range(1, n):
        single_timestep(i)
        time.sleep(0.5)


# to run the app, type in terminal:
#  streamlit run wind_steps_btn_slide.py
