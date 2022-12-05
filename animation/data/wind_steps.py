import pandas as pd
import altair as alt

df = pd.read_csv("./wind.csv")

# add new column for time and set to 0 for all rows
df["time"] = 0
# print(len(df))

# clone df n times (e.g., n = 10, 10 time points)
# only difference between each df clone is time point value, e.g., t = 0, t = 1
n = 5  # how many clones
frames = []  # store dataframes in a list

for t in range(0, n):
    df = df.copy()
    df["time"] = t
    frames.append(df)

# concat all together to one long df
df_times = pd.concat(frames)

# modify the 2 columns: 'dir' and 'speed': dir = dir + x * sin(t/some constant) *the constant gives the period of the sine wave, x gives the amount of flucutation

# df_dynamic = df_times.iloc[23990:23995].copy()
df_dynamic = df_times.copy()
a_dir = 5  # amount of fluctuation
p_dir = 0.5  # period of sine wave

a_speed = 3
p_speed = 5  # period of sine wave

print(df_dynamic.head())
for i in df_dynamic.index:
    df_dynamic.loc[i, "dir"] = df_dynamic.loc[i, "dir"] + a_dir * (
        (df_dynamic.loc[i, "time"]) / p_dir
    )
    df_dynamic.loc[i, "speed"] = df_dynamic.loc[i, "speed"] + a_speed * (
        (df_dynamic.loc[i, "time"]) / p_speed
    )

print(df_dynamic.head())
