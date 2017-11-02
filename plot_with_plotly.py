#==============================================================================
# Do simple plots through plot.ly, such as line plot, histogram, monthly means
# Function names:
#   lineplot()
#   wind_rose_plot()
#   species_histogram()
#==============================================================================
# Uses modules:
# datetime, numpy, pandas, plot.ly, open_DEFRA_csv
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import open_DEFRA_csv.py
import plotly.plotly as py
import plotly.graph_objs as go
#==============================================================================

def line_plot(arg):
    """
        Produces a simple line plot of concentration against time.
    """
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


if __name__ == '__main__':
    filename  = 'Example_Data/' \
                    + 'edinburgh_st_leonards_2015_2017.csv'

## ============================================================================
## END OF PROGAM
## ============================================================================
