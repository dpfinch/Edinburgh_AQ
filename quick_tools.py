#==============================================================================
# Module containing a number of quick and useful tools to be used about for number
# processing
# Function names:
#   round_nearest(num_in)
#   round_up(num_in)
#==============================================================================
# Uses modules:
# math
import math
import brewer2mpl
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
    for cols in bmap:
        R = col[0]
        G = col[1]
        B = col[2]
        colour_array.append('rgb(%d,%d,%d)') % (R,G,B)
    return colour_array

## ============================================================================
## END OF PROGAM
## ============================================================================
