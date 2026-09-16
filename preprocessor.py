import pandas as pd


def preprocess(dataframe, region_dataframe):
    # Keep only Summer Olympics
    dataframe = dataframe[dataframe["Season"] == "Summer"].copy()

    # Merge with regions
    dataframe = dataframe.merge(region_dataframe, on="NOC", how="left")

    # Remove duplicates
    dataframe.drop_duplicates(inplace=True)

    # One-hot encode Medal column
    dataframe = pd.concat(
        [dataframe, pd.get_dummies(dataframe["Medal"], dtype=int)],
        axis=1
    )

    return dataframe