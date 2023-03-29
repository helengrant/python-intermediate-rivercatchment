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
