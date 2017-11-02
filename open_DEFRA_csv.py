#==============================================================================
# Module to read in and clean up AQ data from DEFRA
# e.g. https://uk-air.defra.gov.uk/data/
# Function Names:
#       open_csv(filename, skip_num_rows = 4)
#       select_one_variable(variablename, filename = )
#==============================================================================
# Uses modules:
# datetime, numpy, pandas, os, sys
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os, sys
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
            filepath (REQUIRED, STRING):
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

def select_one_variable(variablename, filename = 'ExampleData'):
    """
        This function reduces the entire data set down to just the species/
        variable that is wanted for a particular analysis. eg. just NO2.
        Function IN:
            variablename(REQUIRED, STRING):
                The name of the species (eg. Nitrogen dioxide)
            filename(OPTIONAL, STRING):
                The path and name of the file. If not chosen then automatically
                uses the example data.
        Function OUT:
            species_data:
                A reduced pandas DataFrame that contains the date and time,
                species concentration, the unit, and the measurement validity
    """

    # If the filename is not set, then use the example data provided
    if filename == 'ExampleData':
        filename = 'Example_Data/edinburgh_st_leonards_2015_2017.csv'
        print "No file specified. Using data from: %s" % filename

    # Check to see whether file  & path exists
    # If it doesn't exist, print warning and exit
    if not os.path.exists(filename):
        print "Unable to open %s \n File doesn't exist."
        sys.exit()


    all_data = open_csv(filename)
    return species_data

if __name__ == '__main__':
    filename  = 'Example_Data/' \
                    + 'edinburgh_st_leonards_2015_2017.csv'

## ============================================================================
## END OF PROGAM
## ============================================================================
