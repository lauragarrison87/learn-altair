# remake of Factfullness bubble chart 
# original data source: https://github.com/open-numbers/ddf--gapminder--systema_globalis
# easy link to geo keys: https://docs.google.com/spreadsheets/d/1qHalit8sXC0R8oVXibc2wa2gY7bkwGzOybEMTWp-08o/edit#gid=425865495 
# original code credits: https://nbviewer.org/github/cereniyim/Plotly-Gapminder-Visualization/blob/master/Factfullness-BubbleChart.ipynb

# import libraries
import pandas as pd

# import data 
life_expectancy = pd.read_csv(
    "https://raw.githubusercontent.com/open-numbers/ddf--gapminder--systema_globalis/master/countries-etc-datapoints/ddf--datapoints--data_quality_life_expectancy--by--geo--time.csv")

income = pd.read_csv(
    "https://raw.githubusercontent.com/open-numbers/ddf--gapminder--systema_globalis/master/countries-etc-datapoints/ddf--datapoints--income_per_person_gdppercapita_ppp_inflation_adjusted--by--geo--time.csv")

population = pd.read_csv(
    "https://raw.githubusercontent.com/open-numbers/ddf--gapminder--systema_globalis/master/countries-etc-datapoints/ddf--datapoints--population_total--by--geo--time.csv")

countries = pd.read_csv(
    "https://raw.githubusercontent.com/open-numbers/ddf--gapminder--systema_globalis/master/ddf--entities--geo--country.csv")
# print(list(countries.columns))
# print(countries['world_4region'].unique())
# print(countries[['country','name','world_4region']].head(10))


# merge dataframes 
gapminder_df = (life_expectancy
                .merge(income, on=["geo", "time"])
                .merge(population, on=["geo", "time"]))

gapminder_df = (gapminder_df
                .merge(
                    countries[["country", "name", "world_4region"]], 
                    left_on="geo", right_on="country"))

# drop unneeded columns and rename remaining
gapminder_df.drop(columns=["country"], inplace=True)

gapminder_df.rename(columns={"name": "Country",
                             "world_4region": "Region",
                             "time": "Year",
                             "life_expectancy_years": "Life Expectancy",
                             "population_total": "Population",
                             "income_per_person_gdppercapita_ppp_inflation_adjusted":
                             "Income",
                             "geo": "Country Code"},
                    inplace=True)

print(gapminder_df.head())
gapminder_df.to_csv('basic_charts_data/gapminder_ddf_1800_2014.csv',index=False)