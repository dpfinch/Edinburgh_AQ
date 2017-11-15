#==============================================================================
# Module to get different types of averaging from a timeseries.
# variables passed can either be a pandas DataFrame or two arrays of time and
# concentration. Maybe also do a dictionary option?
# Function names:
#   convert_to_pandas()
#   running_24_hour()
#   running_8_hour()
#   running_custom_hour()
#==============================================================================
# Uses modules:
# pandas
import pandas as pd
import quick_tools
#==============================================================================

def running_8_hour(timeseries, date_and_time = 'None'):
    """
            Calculates the rolling mean over an 8 hour period. Ideal for ozone
            and CO.
        Function IN:
            timeseries(REQUIRED, PANDAS DATAFRAME or LIST or ARRAY):
                A pandas dataframe of the time series. The time/date elemenet
                must be set as an index for the dataframe. If its a list of a
                numpy array then it will be converted to a pandas DataFrame.
            date_and_time(OPTIONAL, LIST or ARRAY (DATETIME)):
                This is used if the input isn't a pandas dataframe - and is
                two seperate lists of concentration and corresponding date/time.
        Fucntion OUT:
            aved_df:
                The averaged dataframe - this includes mean, std., min, max etc.
    """
    # If the input data is not a pandas timeseries, then try and make it one.
    if not isinstance(timeseries,pd.Series):
        timeseries = quick_tools.convert_to_pandas(timeseries,date_and_time)

    # Get 8 hour rolling stats for the the data.
    # Needs to have a minimum of 75% values (ie 6/8)
    aved_df = timeseries.rolling(8, min_periods = 6)

    return aved_df

def running_24_hour(arg):
    """
            Calculates the rolling mean over an 8 hour period. Ideal for ozone
            and CO.
        Function IN:
            argin(REQUIRED, DTYPE):
                Description of the argument in, wheter its REQUIRED, OPTIONAL,
                or DEFAULT
        Fucntion OUT:
            argout:
                Description of what the fuction returns if any
    """
    pass

def running_custom_hour(arg):
    """
            Calculates the rolling mean over an 8 hour period. Ideal for ozone
            and CO.
        Function IN:
            argin(REQUIRED, DTYPE):
                Description of the argument in, wheter its REQUIRED, OPTIONAL,
                or DEFAULT
        Fucntion OUT:
            argout:
                Description of what the fuction returns if any
    """
    pass

if __name__ == '__main__':
    # If the module needs testing as a stand alone, use this to set the
    # paramters
    filename  = 'Example_Data/' \
                    + 'edinburgh_st_leonards_2015_2017.csv'
    fname(filename)
## ============================================================================
## END OF PROGAM
## ============================================================================
