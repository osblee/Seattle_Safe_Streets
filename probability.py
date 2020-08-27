"""
Osbert Lee, Yui Suzuki, Yukito Shida
CSE 163 Section AA

This file serves to produce quantifiable values that the user can
interpret. Specifically, the probabilities file should be able to
produce the results of a machine learning prediction and also a
confidence interval to test the 911 dials between seasons.
"""
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import scipy.stats as stats


class Probabilities:
    """
    The Probabilities class is a culmination of two separate statistical
    calculations that each provide insight into how we should interpret
    the given data.
    """

    def __init__(self, dataset, address=None, month=None):
        """
        Initalizes the probability class by taking in a location and time.
        If there is no location and time inputted, assume they are None. The
        initialization should also take in the given dataset to be used in the
        future. These values are stored.
        """
        self._df = dataset
        if address is not None:
            self._data = {"address": [address], "datetime": [month]}
            self._address = address
            self._month = month

    def predict(self):
        """
        Uses two machine learning models to determine a prediction based
        on a given dataset, location, and time. The prediction will be
        the likelihood of having a certain type of 911 dial. Function will
        return a tuple of (the type of 911 dial, the percent likeilhood).
        If the inputted location and time are not within the dataset, or if
        the dataset cannot draw meaningful conclusions, the function will
        return a tuple of and empty string and a unrelated percent value.
        Assume that the given month parameter will be a real month.
        Assume case sensitive.
        """
        cleaned = self._df.loc[:, ["datetime", "type", "address"]]
        cleaned["datetime"] = self._df["datetime"].str[5:7].str.lstrip("0")
        cleaned["datetime"] = cleaned['datetime'].astype(int)

        conversion = {1: "January", 2: "February", 3: "March", 4: "April",
                      5: "May", 6: "June", 7: "July", 8: "August",
                      9: "September", 10: "October", 11: "November",
                      12: "December"}
        cleaned["datetime"] = cleaned["datetime"].replace(conversion)

        dt = cleaned[cleaned["address"] == self._address]
        if (len(dt) == 0):
            return ("", 0)

        input_df = pd.DataFrame(self._data)
        features = cleaned.loc[:, ["datetime", "address"]]
        features.append(self._data, ignore_index=True)
        features = pd.get_dummies(features)
        input_df = features.iloc[-1]
        input_df = input_df.values.reshape(1, -1)
        labels = pd.get_dummies(cleaned.loc[:, "type"])
        features_train, features_test, labels_train, labels_test = (
            train_test_split(features, labels, test_size=0.2))

        dtc_model = DecisionTreeClassifier()
        rfc_model = RandomForestClassifier()

        dtc_model.fit(features_train, labels_train)
        rfc_model.fit(features_train, labels_train)
        pred_dtc = dtc_model.predict(features_test)
        pred_rfc = rfc_model.predict(features_test)
        pred_input = rfc_model.predict(input_df)
        accuracy_dtc = accuracy_score(labels_test, pred_dtc)
        accuracy_rtc = accuracy_score(labels_test, pred_rfc)

        average_accuracy = (accuracy_dtc + accuracy_rtc) / 2 * 100
        percent = str(average_accuracy)

        index = np.where(pred_input == 1.)
        if len(index[0]) == 0:
            return ("", percent)
        else:
            index = index[1][0]
            name = labels.columns[index]
            return (name, percent)

    def conf_interval(self):
        """
        Computes and prints out the 95% confidence interval of
        proportion of cases in the spring months vs the proportion
        of cases in the fall months
        """
        cleaned = self._df.loc[:, ["datetime"]]
        cleaned["datetime"] = self._df["datetime"].str[5:7].str.lstrip("0")
        cleaned["datetime"] = cleaned['datetime'].astype(int)

        shuffle = cleaned.sample(frac=1)
        result = np.array_split(shuffle, 2)
        spring_data = result[0].head(100)
        fall_data = result[1].head(100)

        spring = (spring_data["datetime"] == 3) | (
            spring_data["datetime"] == 4) | (spring_data["datetime"] == 5)

        fall = (fall_data["datetime"] == 9) | (
            fall_data["datetime"] == 10) | (fall_data["datetime"] == 11)

        spring_size = spring_data[spring].size
        fall_size = fall_data[fall].size
        confidence = 0.95
        spring_total = 100
        fall_total = 100
        prop_spring = float(spring_size) / spring_total
        prop_fall = float(fall_size) / fall_total
        var = prop_spring * (1 - prop_spring) / spring_total + \
            prop_fall * (1 - prop_fall) / fall_total
        se = np.sqrt(var)
        significance = 1 - confidence
        z = stats.norm(loc=0, scale=1).ppf(confidence + significance / 2)
        prop_diff = prop_spring - prop_fall
        confint = prop_diff + np.array([-1, 1]) * z * se
        return list(confint)
