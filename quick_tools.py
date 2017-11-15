#==============================================================================
# Module containing a number of quick and useful tools to be used about for number
# processing
# Function names:
#   round_nearest(num_in)
#   round_up(num_in)
#   get_colours_rgb(num_colours)
#  convert_to_pandas()
#==============================================================================
# Uses modules:
# math
import math
import brewer2mpl
import pandas as pd
#==============================================================================

def round_nearest(in_num, base = 10):
    """
        Round a number to the nearest specified whole number (ie 8.7 -> 10)
        Function IN:
            in_num (REQUIRED, INTEGER OR FLOAT):
                Number to be rounded
            base (OPTIONAL, INTEGER):
                Number to be rounded to (default = 10)
        Fucntion OUT:
            rounded_num:
                The rounded number.
    """
    rounded_num = int(base * round(float(in_num)/base))
    return rounded_num

def round_up(in_num, base = 10):
    """
        Round a number up to the nearest specified whole number (ie 3 -> 10)
        Function IN:
            in_num (REQUIRED, INTEGER OR FLOAT):
                Number to be rounded
            base (OPTIONAL, INTEGER):
                Number to be rounded to (default = 10)
        Fucntion OUT:
            rounded_num:
                The rounded number.
    """

    rounded_num = int(math.ceil(float(in_num) / base)) * base

    return rounded_num

def get_colours_rgb(num_colours = 8):
    """
        Return an array of colours as an RGB string to use - the size of array
        depends on requested by the user.
        Function IN:
            num_colours (OPTIONAL, INTEGER ):
                The number of colours needed (default = 8)
        Fucntion OUT:
            colour_array:
                An an array containing the number of colours requested as
                RGB string.
    """

    bmap = brewer2mpl.get_map('Blues', 'Sequential', num_colours)
    colour_array = []
    # Loop through all the colours and make them a string
    for col in reversed(bmap.colors):
        R = col[0]
        G = col[1]
        B = col[2]
        colour_array.append('rgb(%d,%d,%d)' % (R,G,B) )
    return colour_array


def convert_to_pandas(data,date_and_time='None'):
    """
            Converts the given data into a pandas DataFrame for ease of use later.
        Function IN:
            data(REQUIRED, LIST or ARRAY(INT or FLOAT):
                The data to be made into the pandas DataFrame. Usually a series
                of concentration.
            date_and_time(OPTIONAL, DATETIME OR STRING):
                A time series corresponding to the data to be converted. Must be
                in a format that pandas will understand. If left then no time data
                will be used (this will limited analysis).
        Fucntion OUT:
            new_dataframe:
                A pandas dataframe of the concentration. Ideally with the index
                being datetime.
    """
    # Test if a datetime is given, if not then don't include it!
    if date_and_time == 'None':
        new_dataframe = pd.DataFrame(data)

    else:
        # Create the data frame with given variables
        new_dataframe = pd.DataFrame({'Data':data,'date_and_time':date_and_time})
        # Make the datetime variable into a datetime format. This might not work
        # and will depend on the way the input was - pandas will complain.
        new_dataframe['date_and_time'] = pd.to_datetime(new_dataframe['date_and_time'])
        # Make the datetime variable the index of the DataFrame.
        new_dataframe.index = new_dataframe.pop('date_and_time')

    return new_dataframe

class DEFRA_site_info(object):
    """
        Return an object which has the information about the DEFRA sites.
        This information is from a csv file. Which in turn is made from
        DEFRA_AURN_data_scrape.py
        Will return object instances:
            Latitude
            Longitude
            Altitude_metres
            UK_AIR_ID
            EU_Site_ID
            Easting
            Northing
            Site_Code
            Site_Address
            Government_Region
    """
    def __init__(self, site_name = 'Edinburgh St Leonards', filename = 'None'):
        super(DEFRA_site_info, self).__init__()
        self.site_name = site_name
        self.filename = filename
        self.get_info()

    def get_info(self):
        # If the file is not set then use the standard - this is currently hard coded
        # and therefore not useable for anyone else
        if self.filename == 'None':
            self.filename = '/home/dfinch/Documents/AQ_datasets/DEFRA_AURN_sites_info.csv'

        # read the csv into a pandas DataFrame
        df = pd.read_csv(self.filename)
        # Make the site name the index
        df.index = df.pop('Site Name')
        # Get the site
        site_info = df.loc[self.site_name]
        self.Latitude = site_info.loc['Latitude']
        self.Longitude = site_info.loc['Longitude']
        self.Altitude_metres = site_info.loc['Altitude (metres)']
        self.UK_AIR_ID = site_info.loc['UK-AIR ID']
        self.EU_Site_ID = site_info.loc['EU Site ID']
        self.Easting = site_info.loc['Easting']
        self.Northing = site_info.loc['Northing']
        self.Site_Code = site_info.loc['Site Code']
        self.Site_Address = site_info.loc['Site Address']
        self.Government_Region = site_info.loc['Government Region']
        self.Site_Code = site_info.loc['Site Code']

        return self

## ============================================================================
## END OF PROGAM
## ============================================================================
