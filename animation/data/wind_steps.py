import pandas as pd
import altair as alt

df = pd.read_csv("./wind.csv")

df["timestep"] = 0  # create new column for timestep in dataframe

# clone df n times (e.g., n = 10, 10 time points)
n = 5  # how many clones
frames = []

for t in range(0, n):
    df = df.copy()
    df["timestep"] = t
    frames.append(df)

# combine individ dfs to one huge dataframe
df_times = pd.concat(frames)

# add some noise as a sine function to dir and speed attributes of dataframe
# df_dynamic = df_times.iloc[23990:23995].copy()
df_dynamic = df_times.copy()

# dir adjustments
a_dir = 5  # amount of fluctuation
p_dir = 0.5  # period of sine wave

# speed adjustments
a_speed = 3
p_speed = 5

for i in df_dynamic.index:
    df_dynamic.loc[i, "dir"] = df_dynamic.loc[i, "dir"] + a_dir * (
        (df_dynamic.loc[i, "timestep"]) / p_dir
    )
    df_dynamic.loc[i, "speed"] = df_dynamic.loc[i, "speed"] + a_speed * (
        (df_dynamic.loc[i, "timestep"]) / p_speed
    )

print(df_dynamic.head())

# check altair graph in static step
# from https://altair-viz.github.io/gallery/wind_vector_map.html example on Vega-Altair documentation site
source = df_dynamic.loc[df_dynamic["timestep"] == 2]
alt.Chart(source).mark_point(shape="wedge", filled=True).encode(
    latitude="latitude",
    longitude="longitude",
    color=alt.Color(
        "dir", scale=alt.Scale(domain=[0, 360], scheme="viridis"), legend=None
    ),
    angle=alt.Angle("dir", scale=alt.Scale(domain=[0, 360], range=[180, 540])),
    size=alt.Size("speed", scale=alt.Scale(rangeMax=500)),
).project("equalEarth").show()
