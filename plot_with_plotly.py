#==============================================================================
# Do simple plots through plot.ly, such as line plot, histogram, monthly means
# Function names:
#   timeseries_plot()
#   wind_rose_plot()
#   species_histogram()
#   monthly_box_plots()
#==============================================================================
# Uses modules:
# datetime, numpy, pandas, plot.ly, open_DEFRA_csv
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import source_AQ_data
import plotly.plotly as py
import plotly.graph_objs as go
#==============================================================================

def timeseries_plot(species='None',filename = 'ExampleData', average = 'None',
    verfied = True):
    """
        Produces a simple line plot of concentration against time.
        Function IN:
            species (REQUIRED, STRING):
                The name of the species you want to plot.
            filename(OPTIONAL, STRING):
                The name of the raw data file, if left it just uses
                example data
            average(OPTIONAL, STRING):
                Choose what type of averaging to use. Choices are None (default),
                8-hour, daily, weekly, monthly
            verfied(OPTIONAL, BOOLEAN):
                Choose whether to plot just verfied data or all data.
                Default = True
    """
    # Get the data for the species required. Also include the filename
    # if the filename is provided - use example data if not.
    # Also returns variable name (this might be changed slightly from user input)
    species_data, variablename = source_AQ_data.select_one_variable(species, filename)

    # If just using verfied data then purge unverified data
    if verfied:
        species_data = source_AQ_data.purge_unverified(species_data, variablename)

    # Set the data in a format the plot.ly needs to work
    data = go.Scatter(x = species_data.index, y = species_data[variablename],
        mode = 'markers')
    data = [data]

    # Set the layout for the plot.ly graph
    layout = go.Layout(
        title = 'Concentration of ' + variablename + ' at Edinburgh St leonards',
        xaxis = dict(title = 'Date and Time'),
        yaxis = dict(title = variablename + ' ('+species_data['Unit'][0]+')'))

    # Set the filename & combine data and layout
    filename = '%s_timeseries' % variablename
    fig = go.Figure(data = data, layout = layout)
    py.plot(fig,filename = filename)

    pass

def wind_rose_plot(arg):
    """
        Procuduces a wind rose plot of wind speed and direction.
    """
    pass

def species_histogram(arg):
    """
        Produces a histogram of concentration of a species.
    """
    pass

def monthly_box_plots(arg):
    """
        Produces box plots of mean, std dev, percentiles of species per month.
    """
    pass

if __name__ == '__main__':
    data = source_AQ_data.select_one_variable('Ozone')

## ============================================================================
## END OF PROGAM
## ============================================================================
