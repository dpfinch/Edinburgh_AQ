#==============================================================================
# Module to read in and clean up AQ data from DEFRA
# e.g. https://uk-air.defra.gov.uk/data/
# Function Names:
#       open_csv(filename, skip_num_rows = 4)
#==============================================================================
# Uses modules:
# datetime, numpy, pandas
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
#==============================================================================
def open_csv(filepath, skip_num_rows = 4):
    """
        This function reads in the CSV file and puts it into a pandas DataFrame.
        Currently only specifically works for DEFRA CSV as they have preamble
        in the files.
        Skips the first four lines of preamble until the column headers.
        Has numerous 'Status' columns - as in status for each measurements,
        these are numbered Status, Status.1, Status.2 etc.
        Function IN:
            filepath (REQUIRED. STRING):
                    path and name of csv file (eg /home/user/myfiles/AirQuality.csv)
            skip_num_rows(DEFAULT = 4, INTEGER):
                    Number of lines to skip of the file, usually 4 for DEFRA
        Function OUT:
            df:
                DataFrame from pandas modules. Will be in pandas format.
                Similar to python dictionaries but with more functions
    """
    # Read straight into pandas data frame
    # Skipping first four lines
    # Needs datatype (dtype) as string since columns mix datatypes
    df =  pd.read_csv(filepath, skiprows = int(skip_num_rows), dtype = str)
    # Get all the column names
    column_names = df.columns
    # Loop through each column and repace 'No data' with NaNs
    # - easier to process into numbers not strings
    for column in column_names:
        df[column].replace('No data', np.nan, inplace = True)
        # In the time column replace the hour 24 with zero
        # This is needed for pandas to convert to a datetime type
        if column == 'Time':
            df[column].replace('24:00:00', '00:00:00', inplace = True)
        # Find if the column is a status column or date/time column, if it
        # is the then go to next iteration, if its not then turn that value
        # from a string into a float
        if column.split('.')[0] == 'Status':
            continue
        elif column in ['Date', 'Time']:
            continue
        else:
            df[column] = df[column].astype(float)

    # Add a new column using both date and time into a datetime format
    df['Date and Time'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

    return df


if __name__ == '__main__':
    filename  = 'Example_Data/' \
                    + 'edinburgh_st_leonards_2015_2017.csv'

## ============================================================================
## END OF PROGAM
## ============================================================================
