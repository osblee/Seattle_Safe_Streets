"""
Osbert Lee, Yui Suzuki, Yukito Shida
CSE 163 Section AA

This file implements the Graph class with two different methods of showing
off our data in an easily consumable way.
Implements two different methods that use the same dataset to create two
separate visualizations. These visualizations are both interactable and very
informative. One graphic should represent an interactable bar chart and the
other should implement an interactable scatter plot.
"""
import plotly.graph_objects as go
import plotly.express as px


class Graph:
    """
    The Graph class will provide two methods of visualizing the dataset
    provided of the 911 fire calls in Seattle. These graphics will allow
    the user to get a stronger understanding of their enviroment and see
    different trends that they can take into consideration over the
    timeframe of a year.
    """

    def __init__(self, dataset):
        """
        Recieves an input of the given dataset and stores this information for
        other methods to use in the future.
        """
        self._df = dataset

    def display_scatter(self):
        """
        Creates an interactable graph of the number of 911 dials of each type
        per each Month. In the graph, the user can select or deselct each type
        to view them. Outputs the graph and displays it on the browser locally.
        """
        cleaned = self._df.loc[:, ["datetime", "type"]]
        cleaned["datetime"] = self._df["datetime"].str[5:7].str.lstrip("0")
        cleaned["datetime"] = cleaned['datetime'].astype(int)
        filtered_df = cleaned.groupby(
            ["datetime", "type"]).size().reset_index(name='count')

        fig = px.scatter(filtered_df, x="datetime", y="count",
                         color="type")

        fig.update_layout(
            title="Distribution of 911 Dials Based on Type of Call per Month",
            xaxis_title="Months",
            yaxis_title="Amount of 911 Dials"

        )
        fig.update_xaxes(
            tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ticktext=['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October',
                      'November', 'December'],
        )
        fig.show()

    def display_bar(self):
        """
        Creates an interactable bar graph displaying the percent of incidents
        reported each month, to the total cases reported. Outputs the
        interactable bar graph locally and opens it auotmatically on browser.
        """
        cleaned = self._df.loc[:, ["datetime", "type"]]
        cleaned["datetime"] = self._df["datetime"].str[5:7].str.lstrip("0")
        cleaned["datetime"] = cleaned['datetime'].astype(int)

        cleaned["count"] = cleaned.groupby("datetime").count()

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        cases = cleaned["count"].dropna().tolist()

        total = sum(cases)

        for i in range(len(cases)):
            cases[i] = cases[i] / total * 100

        fig = go.Figure([go.Bar(x=months, y=cases)])
        fig.update_layout(
            title="Percent of Seattle Incident Reports per Month",
            xaxis_title="Months",
            yaxis_title="Percent of Total Incidents"
        )
        fig.show()
