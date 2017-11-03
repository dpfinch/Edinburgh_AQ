#==============================================================================
# Module to read in and clean up AQ data from DEFRA in their standard csv file.
# e.g. https://uk-air.defra.gov.uk/data/
# Function Names:
#       open_csv(filename, skip_num_rows = 4)
#       select_one_variable(variablename, filename = 'ExampleData')
#       purge_unverified()
#       list_availble_species(all_df_variables)
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
        # This creates an error in the data as the value for 00:00:00 in then
        # placed at the beginning of the day instead of the end. ie. It should
        # changed to 00:00:00 and the date moved forward one day. This is
        # recitifed later.
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
    df['Date and Time'] = df['Date and Time'].apply(add_day)
    return df

def add_day(timestamp):
    """
        This functions fixes the errror in the timeseries where converting the
        the hour '24:00:00' to '00:00:00' put the time at the beginning of the
        day instead of the end. It basically just adds a day where the hour == 0
        Function IN:
            timestap(REQUIRED, DATETIME)
        Function OUT:
            timestap(DATETIME)
    """
    if timestamp.hour == 0:
        timestamp = timestamp + timedelta(days = 1 )
    return timestamp



def select_one_variable(variablename = 'species', filename = 'ExampleData'):
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
        print "No file specified. Using data from: %s \n" % filename

    # Check to see whether file  & path exists
    # If it doesn't exist, print warning and exit
    if not os.path.exists(filename):
        print "Unable to open %s \n File doesn't exist." % filename
        sys.exit()

    # Request all the data from the file
    all_data = open_csv(filename)

    # Check if species requested is available, if not then call user to
    # pick one that is
    if variablename not in all_data.columns:
        variablename = list_availble_species(all_data.columns)

    date_and_time = all_data['Date and Time']
    species_data = all_data[variablename]
    # Need to find the location of the variablename in the list of
    # DataFrame columns - because the one after it is the 'status' that
    # related the that species
    var_location = np.where(all_data.columns == variablename)
    variable_status_name = all_data.columns[np.squeeze(var_location) + 1]
    variable_status = all_data[variable_status_name]
    # Split the status column into 'verified' and 'units'
    # First test to see how if there is any other info in this colum
    # (like '(TEOM FDMS)' - I assume this is an instrument name)
    if len(variable_status[0].split()) > 2:
        verified, units, other = variable_status.str.split(' ',2).str
    else:
        verified, units = variable_status.str.split(' ',1).str

    # Put all the data back into one DataFrame
    species_data = pd.DataFrame({'Date and Time':date_and_time,
        variablename:species_data,'Unit':units,'Verified':verified})

    # Make the DataFrame index be data and time instead of just a count
    species_data.index = species_data.pop('Date and Time')

    return species_data

def purge_unverified(species_data):
    """
        This function removes any measurements that have not been verfied.
        This is indicated by a V (verfied), N (not verified), P (provisional),
        or S (suspect).
        This will replace values of V with NaNs unless the variable is modelled
        (eg. wind speed) as all this is not verified because its not a physical
        measurement.
        Function IN:
            The pandas DataFrame that is to be ammended
            (has to have 'Verified' column in DataFrame)
        Function OUT:
            The same DataFrame but with unverified values replaced with NaNs
    """
    if species.split()[0] == 'Modelled':
        print "Using all data as this data is modelled."
        return species_data
    else:
        verfied_data = species_data['Verified' == 'V']
        return verfied_data


def list_availble_species(all_df_variables):
    """
        This functions lists all the species that are avaible for analysis.
        It requires a user input to pick a species, or write the name.
        The user may also exit the program if they wish.
        Function IN:
            all_df_variables(REQUIRED, LIST):
                A list of all the column (variable) names from the pandas
                dataframe which will be cleaned and printed.
        Function OUT:
            chosen_species:
                The species chosen by the user as string (ie 'PM2.5')
    """
    # Create empty list for species you can choose to go into
    species_list = []
    # Create list of names not wanted (ie stuff that isn't species)
    # This is an inelegant way of doing this but I can't think of another way
    # This list can be added to if need be
    not_species = ['Date','Time', 'Date and Time','Status']
    # Add all chooseable species to a list
    for names in all_df_variables:
        if names.split('.')[0] in not_species:
            continue
        species_list.append(names)
    # Print out all the options with corresponding number
    print 'Availble variables to choose from file: \n'
    for x, names in enumerate(species_list):
        print '%d) %s' % (x + 1, names)

    # Get user to pick species, keep in a loop until something availble is
    # chosen or 'q' is chosen to exit program.
    species_avail = False
    while not species_avail:
        print 'Pick a number from above or type variable (case sensitive):'
        print "Type 'q' to exit."
        user_choice = raw_input('--> ')
        # Test if integer or string.
        try:
            int(user_choice)
            # Check its not a zero or below
            if int(user_choice) < 1:
                print "%d is out of range." % int(user_choice)
                continue
            number_choice = int(user_choice) - 1 # Need to subtract for python index
            try:
                chosen_species = species_list[number_choice]
                species_avail = True
            except IndexError:
                print "%d is out of range." % int(user_choice)
        except ValueError:
            # If 'q' then exit.
            if user_choice == 'q':
                sys.exit()
            # If user choice is in the species_list then we're cooking.
            elif user_choice in species_list:
                chosen_species = user_choice
                species_avail = True
            else:
                # If it doesn't match anything send them round again.
                print "Species not availble (captials must match)"

    return chosen_species

if __name__ == '__main__':
    filename  = 'Example_Data/' \
                    + 'edinburgh_st_leonards_2015_2017.csv'

## ============================================================================
## END OF PROGAM
## ============================================================================
