"""
Osbert Lee, Yui Suzuki, Yukito Shida
CSE 163 Section AA

This file contains the implementation of the Map class used in our
program. The map class is able to create two types of maps, one
at a city level and another at a street level.
"""
from sodapy import Socrata
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.plotting import gmap
import pandas as pd


class Map:
    """
    The Map class can plot incidents in the entire city of Seattle onto
    an interactive google map. The class can also take in a street name
    and produce a zoomed in google maps with 911 calls in the vicinity of
    the given street. In each case, produces an HTML file with the interactive
    map.
    """

    def __init__(self, location=None):
        """
        Recieves the input street name if there is any called, and retrieves
        the incident information api from "data.seattle.gov" and converts
        it into a dataframe object.
        Assume case sensitive.
        """
        self._location = location

        client = Socrata("data.seattle.gov", None)
        results = client.get("kzjm-xkqj", limit=2000)
        self._df = pd.DataFrame.from_records(results)

    def create_all(self):
        """
        Creates a map with all incident reports plotted onto a google maps
        of Seattle. The map is interactive, and the output file is an HTML
        document "gmap.html"
        """
        output_file("gmap.html")
        map_options = GMapOptions(
            lat=47.608013, lng=-122.335167, map_type="roadmap", zoom=12)
        p = gmap("AIzaSyCaSPqCN6IgZb_vqQZ0F10LmiyK_QXd5sM", map_options,
                 title="Seattle", plot_width=1000, plot_height=1000)
        for streets in self._df["address"].unique():
            is_street = self._df["address"] == streets
            latitude = self._df[is_street].loc[:, "latitude"]
            longitude = self._df[is_street].loc[:, "longitude"]
            source = ColumnDataSource(
                data=dict(lat=[latitude], lon=[longitude]))
            p.circle(x="lon", y="lat", size=10, fill_color="blue",
                     fill_alpha=0.8, source=source)
        show(p)

    def valid_street(self):
        """
        Return whether the street is a valid street
        """
        if (self._location == ""):
            return False
        dt = self._df[self._df["address"] == self._location]
        x = len(dt)
        return (x > 0)

    def g_street(self):
        """
        Creates a map, zoomed into a given street name. The surrounding few
        blocks will have incidents plotted. The output is an HTML document
        with an interactive google maps, named "gstreet.html".
        """
        radius = 0.005
        is_street = self._df["address"] == self._location
        latitude = (self._df[is_street]["latitude"].iloc[0])
        longitude = (self._df[is_street]["longitude"].iloc[0])
        output_file("gstreet.html")
        map_options = GMapOptions(
            lat=float(latitude),
            lng=float(longitude),
            map_type="roadmap",
            zoom=16)
        p = gmap("AIzaSyCaSPqCN6IgZb_vqQZ0F10LmiyK_QXd5sM", map_options,
                 title="Seattle", plot_width=1000, plot_height=1000)

        x1 = (self._df["latitude"] <= str(
            float(latitude) + radius).decode('utf8'))
        x2 = (self._df["latitude"] >= str(
            float(latitude) - radius).decode('utf8'))
        y1 = (self._df["longitude"] >= str(
            float(longitude) + radius).decode('utf8'))
        y2 = (self._df["longitude"] <= str(
            float(longitude) - radius).decode('utf8'))
        filtered = self._df[x1 & x2 & y1 & y2]
        f_lat = filtered.loc[:, "latitude"]
        f_lon = filtered.loc[:, "longitude"]
        source = ColumnDataSource(data=dict(lat=f_lat, lon=f_lon))
        p.circle(x="lon", y="lat", size=15, fill_color="red",
                 fill_alpha=0.8, source=source)
        show(p)

    def dataset(self):
        """
        Getter method for the dataset
        """
        return self._df
