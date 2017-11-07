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


if __name__ == '__main__':
    # If the module needs testing as a stand alone, use this to set the
    # paramters
    filename  = 'Example_Data/' \
                    + 'edinburgh_st_leonards_2015_2017.csv'
    fname(filename)
## ============================================================================
## END OF PROGAM
## ============================================================================
