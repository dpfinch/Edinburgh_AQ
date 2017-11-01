#==============================================================================
# Module to read in and clean up AQ data from DEFRA
# e.g. https://uk-air.defra.gov.uk/data/
#==============================================================================
# Import relevant modules
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
#==============================================================================

def open_csv(filepath):
    """
        This function reads in the CSV file and puts it into a pandas DataFrame.
        Currently only specifically works for DEFRA CSV as they have preamble
        in the files.
        Skips the first four lines of preamble until the column headers.
        Has numerous 'Status' columns - as in status for each measurements,
        these are numbered Status, Status.1, Status.2 etc.
    """
    # Read straight into pandas data frame
    # Skipping first four lines
    # Needs datatype (dtype) as string since columns mix datatypes
    df =  pd.read_csv(filepath, skiprows = 4, dtype = str)
    # Get all the column names
    column_names = df.coloumns
    # Loop through each column and repace 'No Data' with NaNs
    # - easier to process into numbers not strings
    for column in column_names:
        df[column].replace('No Data', np.nan, inplace = True)


    return df


if __name__ == '__main__':
    filename  = 'Example_Data/' \
                    + 'edinburgh_st_leonards_2015_2017.csv'

## ============================================================================
## END OF PROGAM
## ============================================================================
