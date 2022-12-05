import pandas as pd

df = pd.read_csv("./src/BioVis-challenge-test-data.csv")
print(df.head())

residues = df["RES"].unique()
mods = df["MOD"].unique()
types = df["classification"].unique()

print(types)
