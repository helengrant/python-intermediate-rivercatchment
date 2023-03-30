# RiverCatch

![Continuous Integration build in GitHub actions](https://github.com/helengrant/python-intermediate-rivercatchment/workflows/CI/badge.svg?branch=develop)

RiverCatch is a data management system written in python that manages data measured in river catchment surveys and campaigns.

## Main Features
Here are some key features of Inflam:

- provide basic statistical analyses of data
- Ability to work on measurement data in Comma-Separated-Value (CSV) format
- Generate plots of measurement data
- Analytical functions and views can be easily extended based on its Model-View-Controller architecture

- [NumPy](https://www.numpy.org/) - makes use of NumPy's statistical functions
- [Pandas](https://pandas.pydata.org/) - makes use of Panda's dataframes
- [GeoPandas](https://geopandas.org/) - makes use of GeoPanda's 
- [Matplotlib](https://matplotlib.org/stable/index.html) - uses Matplotlib to generate statistical plots

The following optional packages are required to run RiverCatch's unit tests:

- [pytest](https://docs.pytest.org/en/stable/) - RiverCatch's unit tests are written using pytest
- [pytest-cov](https://pypi.org/project/pytest-cov/) - Adds test coverage stats to unit testing