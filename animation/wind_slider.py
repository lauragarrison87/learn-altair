import pandas as pd
import altair as alt
import streamlit as st
import numpy as np

n = 100  # how many time steps


@st.cache  # performance optimization for data load (see https://docs.streamlit.io/library/advanced-features/caching)
def get_data(mydata):
    df = pd.read_csv(mydata)

    df["timestep"] = 0  # create new column for timestep in dataframe

    frames = [df]

    for t in range(1, n + 1):
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
    df_dynamic.loc[:, "speed"] += a_speed
    print(df_dynamic.head())

    return df_dynamic


# from https://altair-viz.github.io/gallery/wind_vector_map.html example on Vega-Altair documentation site
source = get_data("./data/wind.csv")
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


# build streamlit interface
slider_value = st.slider("Choose a timestep", min_value=0, max_value=n, value=0)
st.write(slider_value)


def single_timestep(i):
    step_df = source.loc[source["timestep"] == i]
    chart = animate(step_df)
    st.altair_chart(chart)


single_timestep(slider_value)


# to run the app, type in terminal:
#  streamlit run wind_steps_slider.py
