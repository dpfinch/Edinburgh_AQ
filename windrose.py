#==============================================================================
# Take windspeeds and directions and converts into format usuable for a
# windrose plot
# Function names:
#   windrose(windspeed, winddirection)
#==============================================================================
# Uses modules:
# numpy, sys, pandas, quick_tools
import numpy as np
import sys
import pandas as pd
import quick_tools import round_up
#==============================================================================

def windrose(windspeed, winddirection, direction_bin_size = 8,
    speed_bin_size = 4):
    """
        Description of function here
        Function IN:
            windspeed (REQUIRED, FLOAT/INT, LIST or PANDAS Series):
                An array (or list) holding the wind speed data as either a float
                or integer.
            winddirection (REQUIRED, FLOAT/INT, LIST or PANDAS Series):
                An array (or list) holding the wind direction data as either a float
                or integer
            direction_bin_size (OPTIONAL, INTEGER):
                Choose how many leaves of the windrose you want. Default 8
                (ie. 'North', 'NE', 'East', 'SE', 'South', 'SW', 'West', 'NW').
                Choose 4, 8 or 16
            speed_bin_size (OPTIONAL, INTEGER);
                Choose the size of the bins for the wind speed. Default is 4 (m/s)
        Fucntion OUT:
            windrose_data:
                The data formatted to plot a windrose. Mainly in the format to use
                for plot.ly windrose plot but hopefully not exclusively.
    """

    # Test to see if bins is currently something that can be caluclated
    # Could change this in the future to be more adaptive.
    if direction_bin_size not in [4,8,16]:
        print "Cannot compute %d bins, choose 4, 8 or 16"
        sys.exit()
    # Test to see if wind speed an direction are same length
    if len(windspeed) != len(winddirection):
        print "Wind speed and direction not same length and need to be."
        print "Wind speed has length %d and direction has length %d" % (len(windspeed), len(winddirection))
        sys.exit()

    # Get length of data and max wind speed
    datalen = len(windspeed)
    wind_max = max(windspeed)
    # Set the names for the dirction bins for the plot
    dirc_categories = ['North', 'NNE', 'NE', 'ENE', 'East', 'ESE', 'SE',
        'SSE', 'South', 'SSW', 'SW', 'WSW', 'West', 'WNW', 'NW', 'NNW']

    # Make a limit for the wind speed bins (ie 25 if max speed is 22).
    # Will round up to the nearest 5. Although this can be adjustested.
    round_base = speed_bin_size
    wind_limit = round_up(wind_max, base = round_base)
    # Make bins for the wind speed
    speed_bins = np.arange(0, wind_limit + round_base, round_base)

    # Reduce the category labels if using 4 or 8 bins
    if direction_bin_size == 4:
        dirc_categories = dirc_categories[::4]
    if direction_bin_size == 8:
        dirc_categories = dirc_categories[::2]

    # Set the number of degrees. Need one more than number of categories
    degs = np.linspace (0,360, len(dirc_categories) + 1)

    # Test if the inputs are lists or pandas DataFrame or numpy.ndarray
    if isinstance(windspeed,list) and isinstance(winddirection,list):
        islist = True
    elif isinstance(windspeed,pd.Series) and isinstance(winddirection,pd.Series):
        islist = False
    elif isinstance(windspeed,np.ndarray) and isinstance(winddirection,np.ndarray):
        islist = True
    else:
        print "Input format not recognised. Use list, numpy.ndarray or pandas series"
        print "Both wind speed and direction need to be same format."
        sys.exit()
    # Make a dictionary  of the wind directions and
    # put the windspeeds into the categories
    direction_dict = {}
    for n, directions in enumerate(dirc_categories):
        # But the windspeeds that fall into the bin into dictionary
        # If the datatype is a list then do the following:
        if islist:
            wind_s = np.asarray(windspeed)
            wind_d = np.asarray(winddirection)

            temp_bin = wind_s[np.where(x > degs[n] and x < deg[n + 1] for x in wind_d)]
            direction_dict[directions] = temp_bin.tolist()

        # If datatype not a list(and therefore hopefully a pandas series) then:
        else:
            # Select the windspeeds where the winddirection is between two degree values
            temp_bin = windspeed.loc[(winddirection > degs[n]) &
                (winddirection < degs[n + 1])]
            # Add to dictionary.
            direction_dict[directions] = temp_bin.values.tolist()

    # Create a new dictionary binned as windspeed
    # Create dictionary keys of all the windspeeds with empty lists
    windrose_data = {}
    speed_bin_names = []
    for n, directions in enumerate(dirc_categories):
        # Use numpy.histogram to create histogram of speeds in this bin.
        # As this returns [numbers][bins] - get first from list (ie [numbers])
        temp_hist = np.histogram(direction_dict[directions], speed_bins)[0]
        hist_perc = temp_hist / float(datalen) * 100

        # Need to make the percentes add up cumultively for plotting purposes
        hist_perc = np.cumsum(hist_perc)

        for x, sb in enumerate(speed_bins[:-1]):
            if x == 0:
                bin_name = "< %d m/s" % speed_bins[x + 1]
            elif x == (len(speed_bins) - 1):
                bin_name = "> %d m/s" % speed_bins[x]
            else:
                bin_name = "%d-%d m/s" % (speed_bins[x], speed_bins[x + 1])

            if bin_name not in windrose_data.keys():
                speed_bin_names.append(bin_name)
                windrose_data[bin_name] = []

            # Append the histogram percentage into the correct bin.
            # Round percentage to two decimal places
            windrose_data[bin_name].append(round(hist_perc[x],2))

    # Add extra key to dictionary that explains the order of directions
    windrose_data['Direction'] = dirc_categories
    return windrose_data, speed_bin_names

if __name__ == '__main__':
    # If the module needs testing as a stand alone, use this to set the
    # paramters
    filename  = 'Example_Data/' \
                    + 'edinburgh_st_leonards_2015_2017.csv'
    fname(filename)
## ============================================================================
## END OF PROGAM
## ============================================================================
