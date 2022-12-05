import pandas as pd
import altair as alt
import streamlit as st
import numpy as np
import time

n = 100  # how many time steps


@st.cache
def get_data(mydata):
    df = pd.read_csv(mydata)

    df["timestep"] = 0  # create new column for timestep in dataframe

    # clone df n times (e.g., n = 10, 10 time points)
    frames = [df]

    for t in range(1, n):
        df = df.copy()
        df["timestep"] = t
        frames.append(df)

    # combine individ dfs to one huge dataframe
    df_times = pd.concat(frames)

    # add some noise as a sine function to dir and speed attributes of dataframe
    # df_dynamic = df_times.iloc[23990:23995].copy()
    df_dynamic = df_times

    # dir adjustments
    a_dir = 50  # amount of fluctuation
    # speed adjustments
    a_speed = 3

    w = 2 * np.pi / n  # period of sine wave

    df_dynamic.loc[:, "dir"] += a_dir * np.sin(df_dynamic.loc[:, "timestep"] * w)
    df_dynamic.loc[:, "speed"] += a_speed * np.sin(
        df_dynamic.loc[:, "timestep"] * 2 * w
    )
    df_dynamic.loc[:, "speed"] += a_speed  # keep speed from being below 0
    print(df_dynamic.head())

    return df_dynamic


# check altair graph in static step
# from https://altair-viz.github.io/gallery/wind_vector_map.html example on Vega-Altair documentation site

source = get_data("./wind.csv")
print(source.describe())

# set up chart beginning with t = 0 (this is how the vis will load by default)
def animate(source_time0):
    # source_time0 = source.loc[source["timestep"] == 0]

    chart = (
        alt.Chart(source_time0)
        .mark_point(shape="wedge", filled=True)
        .encode(
            latitude="latitude",
            longitude="longitude",
            color=alt.Color(
                "dir", scale=alt.Scale(domain=[0, 360], scheme="viridis"), legend=None
            ),
            angle=alt.Angle("dir", scale=alt.Scale(domain=[0, 360], range=[180, 540])),
            size=alt.Size("speed", scale=alt.Scale(rangeMax=500)),
        )
        .project("equalEarth")
    )
    return chart


# build streamlit interface
# t = 0:
wind_plot = st.altair_chart(animate(source.loc[source["timestep"] == 0]))
start_btn = st.button("Start")

if start_btn:
    for i in range(1, n):
        step_df = source.loc[source["timestep"] == i]
        chart = animate(step_df)
        wind_plot = wind_plot.altair_chart(chart)
        time.sleep(0.1)


# to run the app, type in terminal:
#  streamlit run wind_steps.py
