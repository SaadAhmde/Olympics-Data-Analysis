import numpy as np
from pandas import pivot_table
from pandas.core.reshape import pivot
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def fetch_medal_tally(dataframe, year, country):

    medal_df = dataframe.drop_duplicates(
        subset=[
            "Team",
            "NOC",
            "Games",
            "Year",
            "City",
            "Sport",
            "Event",
            "Medal"
        ]
    )

    # Overall Year + Overall Country
    if year == "Overall" and country == "Overall":
        temp_df = medal_df

    # Overall Year + Selected Country
    elif year == "Overall" and country != "Overall":
        temp_df = medal_df[
            medal_df["region"] == country
        ]

    # Selected Year + Overall Country
    elif year != "Overall" and country == "Overall":
        temp_df = medal_df[
            medal_df["Year"] == int(year)
        ]

    # Selected Year + Selected Country
    else:
        temp_df = medal_df[
            (medal_df["Year"] == int(year)) &
            (medal_df["region"] == country)
        ]

    # Count medals
    x = (
        temp_df
        .groupby("region")["Medal"]
        .value_counts()
        .unstack(fill_value=0)
    )

    # Make sure all medal columns exist
    for medal in ["Gold", "Silver", "Bronze"]:
        if medal not in x.columns:
            x[medal] = 0

    # Keep required columns
    x = x[["Gold", "Silver", "Bronze"]]

    # Total medals
    x["Total"] = (
        x["Gold"] +
        x["Silver"] +
        x["Bronze"]
    )

    # Sort by Gold medals
    x = x.sort_values(
        "Gold",
        ascending=False
    ).reset_index()

    return x


def year_wise_medal_tally(dataframe, country):

    medal_df = dataframe.drop_duplicates(
        subset=[
            "Team",
            "NOC",
            "Games",
            "Year",
            "City",
            "Sport",
            "Event",
            "Medal"
        ]
    )

    # Filter to the selected country only
    temp_df = medal_df[medal_df["region"] == country]

    # Group by Year instead of region
    x = (
        temp_df
        .groupby("Year")["Medal"]
        .value_counts()
        .unstack(fill_value=0)
    )

    for medal in ["Gold", "Silver", "Bronze"]:
        if medal not in x.columns:
            x[medal] = 0

    x = x[["Gold", "Silver", "Bronze"]]
    x["Total"] = x["Gold"] + x["Silver"] + x["Bronze"]

    x = x.sort_values("Year").reset_index()

    return x


def country_year_list(dataframe):

    year = dataframe["Year"].unique().tolist()
    year.sort()
    year.insert(0, "Overall")

    country = np.unique(
        dataframe["region"].dropna().values
    ).tolist()

    country.sort()
    country.insert(0, "Overall")

    return year, country

def nation_over_time(dataframe):

    nation_over_time = (
        dataframe.drop_duplicates(
            ["Year", "region"]
        )
        .groupby("Year")["region"]
        .nunique()
        .reset_index(name="Nations")
    )

    return nation_over_time

def events_over_time(dataframe):
    events_over_time = (
        dataframe
        .drop_duplicates(["Year", "Event"])
        ["Year"]
        .value_counts()
        .reset_index(name="Events")
        .sort_values("Year")
    )

def athlete_over_time(dataframe):
    athlete_over_time = (
        dataframe
        .drop_duplicates(["Year", "	Name"])
        ["Year"]
        .value_counts()
        .reset_index(name="	Name")
        .sort_values("Year")
    )

def most_success(dataframe, Sport):

    temp_df = dataframe.dropna(subset=["Medal"])

    if Sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == Sport]

    # Count medals for each athlete
    athlete_medals = (
        temp_df["Name"]
        .value_counts()
        .reset_index()
    )

    # Rename columns
    athlete_medals.columns = ["Name", "Medals"]

    # Top 15 athletes
    athlete_medals = athlete_medals.head(15)

    # Get athlete information
    result = athlete_medals.merge(
        dataframe[["Name", "Sport", "region"]],
        on="Name",
        how="left"
    )

    # Remove duplicate athlete rows
    result = result.drop_duplicates("Name")

    return result

def country_medal_tally(dataframe, country):

    country_data = dataframe[dataframe["region"] == country]

    medal_tally = country_data.drop_duplicates(
        subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"]
    )

    medal_tally = (
        medal_tally
        .groupby("Year")[["Gold", "Silver", "Bronze"]]
        .sum()
        .reset_index()
    )

    medal_tally["Total"] = (
        medal_tally["Gold"] +
        medal_tally["Silver"] +
        medal_tally["Bronze"]
    )

    return medal_tally

def country_wise_event_tally(dataframe, country):

    tem_df = dataframe.dropna(subset=["Medal"])

    tem_df = tem_df.drop_duplicates(
        subset=[
            "Team",
            "NOC",
            "Games",
            "Year",
            "City",
            "Sport",
            "Event",
            "Medal"
        ]
    )

    new_data = tem_df[tem_df["region"] == country]

    pivot_table = new_data.pivot_table(
        index="Sport",
        columns="Year",
        values="Medal",
        aggfunc="count"
    ).fillna(0).astype(int)

    plt.figure(figsize=(19, 19))

    sns.heatmap(
        pivot_table,
        annot=True
    )

    return plt.gcf()
def top_10_success_athletes(dataframe, country):

    # Select athletes who won medals
    temp_df = dataframe.dropna(subset=["Medal"])

    # Select the chosen country
    temp_df = temp_df[temp_df["region"] == country]

    # Count medals by athlete
    athlete_medals = (
        temp_df["Name"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    athlete_medals.columns = ["Name", "Medals"]

    # Get the sport of each athlete
    athlete_info = dataframe[["Name", "Sport"]].drop_duplicates("Name")

    result = athlete_medals.merge(
        athlete_info,
        on="Name",
        how="left"
    )

    return result

def age_analysis(dataframe):

    temp_df = dataframe.dropna(subset=["Age", "Medal"]).copy()

    # Average age by medal
    average_age = (
        temp_df.groupby("Medal")["Age"]
        .mean()
        .round(2)
        .reset_index()
    )

    # Age group analysis
    temp_df["Age Group"] = pd.cut(
        temp_df["Age"],
        bins=[0, 15, 20, 25, 30, 35, 40, 100],
        labels=[
            "Under 16", "16-20", "21-25",
            "26-30", "31-35", "36-40", "41+"
        ]
    )

    age_groups = (
        temp_df["Age Group"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    age_groups.columns = ["Age Group", "Medals"]

    return average_age, age_groups