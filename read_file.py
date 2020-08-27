"""
Osbert Lee, Yui Suzuki, Yukito Shida
CSE 163 Section AA

This file is meant to showcase what we would've done to clean our
data if we had the hardware and network capabilities. In this scenario,
we would have looked through all of our data entirely through the API,
and cleaned it so that we only have data from the past 365 days.
"""
import pandas as pd
from sodapy import Socrata


def clean_data():
    """
    This method takes in our API of the dataset and cleans all
    1.5 million 911 fire calls so that the returned dataframe will
    be only calls from the last 365 days.
    """
    client = Socrata("data.seattle.gov", None)

    results = client.get_all("kzjm-xkqj")

    df = pd.DataFrame.from_records(results)
    time = df["datetime"] >= "2019-08-21T00:00:00.000"
    df = df[time]

    cleaned = df.loc[:, ["address", "type", "datetime"]]

    return cleaned
