"""Module containing models representing catchment data.

The Model layer is responsible for the 'business logic' part of the software.

Catchment data is held in a Pandas dataframe (2D array) where each column contains
data for a single measurement site, and each row represents a single measurement
time across all sites.
"""

import pandas as pd
import numpy as np
from functools import reduce


def read_variable_from_csv(filename):
    """Reads a named variable from a CSV file, and returns a
    pandas dataframe containing that variable. The CSV file must contain
    a column of dates, a column of site ID's, and (one or more) columns
    of data - only one of which will be read.

    :param filename: Filename of CSV to load
    :return: 2D array of given variable. Index will be dates,
             Columns will be the individual sites
    """
    dataset = pd.read_csv(filename, usecols=['Date', 'Site', 'Rainfall (mm)'])

    dataset = dataset.rename({'Date': 'OldDate'}, axis='columns')
    dataset['Date'] = [pd.to_datetime(x, dayfirst=True) for x in dataset['OldDate']]
    dataset = dataset.drop('OldDate', axis='columns')

    newdataset = pd.DataFrame(index=dataset['Date'].unique())

    for site in dataset['Site'].unique():
        newdataset[site] = dataset[dataset['Site'] == site].set_index('Date')["Rainfall (mm)"]

    newdataset = newdataset.sort_index()

    return newdataset


def daily_total(data):
    """Calculate the daily total of a 2D data array.

    :param data: A 2D pandas dataframe with measurable data.
                 Index must be np.datetime64 compatible format. Columns are measurement sites.
    :returns: A 2D pandas dataframe with total values of measurement for each day."""
    return data.groupby(data.index.date).sum()


def daily_mean(data):
    """Calculate the daily mean of a 2d data array.
    :param data: A 2D pandas dataframe with measurable data.
                 Index must be np.datetime64 compatible format. Columns are measurement sites.
    :returns: A 2D pandas dataframe with mean values of measurement for each day."""
    return data.groupby(data.index.date).mean()


def daily_max(data):
    """Calculate the daily minimum of a 2D data array.

    :param data: A 2D Pandas data frame with measurement data.
                 Index must be np.datetime64 compatible format. Columns are measurement sites.
    :returns: A 2D Pandas data frame with maximum values of the measurements for each day."""
    return data.groupby(data.index.date).max()


def daily_min(data):
    """Calculate the daily minimum of a 2D data array.

    :param data: A 2D Pandas data frame with measurement data.
                 Index must be np.datetime64 compatible format. Columns are measurement sites.
    :returns: A 2D Pandas data frame with minimum values of the measurements for each day."""
    return data.groupby(data.index.date).min()


def data_normalise(data):
    """Normalise any given 2D array"""
    max_array = np.array(np.max(data, axis=0))
    return data / max_array[np.newaxis, :]


def data_above_threshold(site_id, data, threshold):
    """Determine whether measurement value is above given threshold and count them"""
    def count_above_threshold(a, b):
        if b:
            return a+1
        else:
            return a
    above_threshold = (map(lambda x: x > threshold, data[site_id]))
    return reduce(count_above_threshold, above_threshold, 0)


class MeasurementSeries: # A new class separate from sites that contains the data
    def __init__(self, series, name, units):
        self.series = series # This will be the data
        self.name = name # This will be the name
        self.units = units # This will be the units of the data
        self.series.name = self.name

    def add_measurement(self, data):
        self.series = pd.concat([self.series, data])
        self.series.name = self.name

    def __str__(self): # Make sure printing shows strings rather than data types
        if self.units:
            return f"{self.name} ({self.units})"
        else:
            return self.name


class Location: # A little class of just location name
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

class Site(Location): # Creating a 'site' class that inherits information from the Location
    """A measurement site in the study."""
    version = 0.1

    def __init__(self, name):
        super().__init__(name) # Because we are inheriting a name from the Location class
        self.measurements = {}

    def add_measurement(self, measurement_id, data, units=None):
        if measurement_id in self.measurements.keys():
            self.measurements[measurement_id].add_measurement(data)
        else:
            self.measurements[measurement_id] = MeasurementSeries(data, measurement_id, units)

    @classmethod
    def get_version(cls): # This means you can print the version as a string
        return "version "+str(cls.version)

    @staticmethod
    def create_sample_site():
        return Site("sample")

    def __str__(self): # this is so that if you print name it gives a string not the representation
        return self.name

    @property # You can pretend a function looks like an attribute in your class
    def last_measurements(self): # Essentially a function with no arguments/inputs
        return pd.concat(
            [self.measurements[key][-1:]
             for key in self.measurements.keys()], axis=1).sort_index()


