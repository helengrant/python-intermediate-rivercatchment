import pandas as pd
import numpy as np
from catchment.models import Site
import datetime

data0 = pd.DataFrame([[1.0, 2.0, 3.0],
                     [4.0, 5.0, 6.0]],
                     index=['FP35', 'FP56'])

location_measurement = [
    ("FP", "FP35", "Rainfall"),
    ("FP", "FP56", "River Level"),
    ("PL", "PL23", "River Level"),
    ("PL", "PL23", "Water pH")
]

index_names = ["Catchment", "Site", "Measurement"]
index = pd.MultiIndex.from_tuples(location_measurement, names=index_names)

data = [
    [0., 2., 1.],
    [30., 29., 34.],
    [34., 32., 33.],
    [7.8, 8., 7.9]
]

data2 = pd.DataFrame(data, index=index)
# print(data2)

measurement_data = [
    {
        "site": "FP35",
        "measurement": "Rainfall",
        "data": [0., 2., 1.]
    },
    {
        "site": "FP56",
        "measurement": "River level",
        "data": [30., 29., 34.],
    }
]
# print(measurement_data)

data_ex1 = np.array([[34., 32., 33.],
                     [7.8, 8.0, 7.9]])


def attach_information(data, sites, measurements):
    assert len(data) == len(sites)  # this allows for the prevention of the code running away
    assert len(data) == len(measurements)
    output = []

    for data_row, measurement, site in zip(data, sites, measurements):
        output.append({'site': sites,
                       'measurement': measurements,
                       'data': data_row})

        return output


output = attach_information(data_ex1, ['PL23', 'PL23'], ['River Level', 'pH'])
# print(output)


FP35 = Site('FP35')
rainfall_data = pd.Series(
    [0.0, 2.0, 1.0],
    index=[
        datetime.date(2000, 1, 1),
        datetime.date(2000, 1, 2),
        datetime.date(2000, 1, 3)
        ]
    )
waterph_data = pd.Series(
    [7.8, 8.0, 7.9],
    index=[
        datetime.date(2000, 1, 1),
        datetime.date(2000, 1, 2),
        datetime.date(2000, 1, 3)
        ]
    )
FP35.add_measurement('Rainfall', rainfall_data)
FP35.add_measurement('Water pH', waterph_data)

# last_data = FP35.last_measurements
# print(last_data)

print(FP35.measurements['Rainfall'].series)
PL12 = Location('PL12')
print(PL12)

#PL12.add_measurement('Rain', rainfall_data)

# print(FP35.measurements.krainfalleys())
# print(FP35.measurements['Rainfall'])
# print(Site.get_version())
# default_site = Site.create_sample_site()
# print(default_site.name)
# print(FP35)


#book = Book("A Book", "Me")
# class Book:
#    def __init__(self, title, author):
#        self.title = title
#        self.author = author

#    def __str__(self): # this is so that if you print name it gives a string not the representation
#        return self.title+" by "+self.author
# print(Book)
