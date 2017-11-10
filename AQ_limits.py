#==============================================================================
# Provide information on air quality standards and limits to use in comparisons.
# This uses a CSV file which may need updating every now and again.
# It uses the file 'AQ_limits_database.csv'. information from for this was
# aquired from: https://uk-air.defra.gov.uk/air-pollution/uk-eu-limits
# This module aims to return the air quality limit for a given species at for
# a given time period (eg NO2 DAILY, CO 8-HOURLY, PM10 ANNUAL)
#
#==============================================================================
# Uses modules:
# pandas
import pandas as pd
#==============================================================================

class AQ_limits(object):
    """
        docstring for AQ_limits.
    """
    def __init__(self, species):
        super(AQ_limits, self).__init__()
        self.input_species = species
        self.full_database = self.get_all_limits()
        self.availble_species = [x for x in self.full_database.index]
        self.get_limits()

    def get_all_limits(self):
        """
            Open the AQ limits database file. Uses the file included in the
            package.
        """
        # Set file name & read in with pandas. Skip first row of first headings
        filename = 'AQ_limits_database.csv'
        AQ_df = pd.read_csv(filename, skiprows = 1)
        # Make the species column the DataFrame index
        AQ_df.index = AQ_df.pop('SPECIES')

        return AQ_df

    def check_species_name(self, species_input = 'None'):
        """
            Checks that the input species matches a species in the database.
            Everything in the database is in capitals and the chemical forumla.
            This function will convert input to capitals and test for chemical
            formula or abbv chemical (eg PAH for Poly Aromatic Hydrocarbons).
        """
        # Convert the input into all upper case
        species_upper = species_input.upper()

        # Check if the given species is in the availble_species
        if species_upper in self.availble_species:
            self.species_name = species_upper
            return self
        # Check if it is PM10
        elif species_upper in ['PM10','PM 10','PARTICULATE MATTER 10' ]:
            changed_name = 'PM10'
        # Check if it is PM2.5
        elif species_upper in ['PM25', 'PM 25', 'PM2.5', 'PARTICULATE MATTER 25']:
            changed_name = 'PM2.5'
        # Check if NO2
        elif species_upper in ['NO2', 'NITROGEN DIOXIDE']:
            changed_name = 'NO2'
        # Check if O3
        elif species_upper in ['O3','OZONE']:
            changed_name = 'O3'
        # Check if SO2
        elif species_upper in ['SO2','SULPHUR DIOXIDE','SULFUR DIOXIDE']:
            changed_name = 'SO2'
        # Check if PAH
        elif species_upper in ['PAH','PAHS','POLY AROMATIC HYDROCARBONS']:
            changed_name = 'PAH'
        # Check if CO
        elif species_upper in ['CO','CARBON MONOXIDE']:
            changed_name = 'CO'
        # Check if NO
        elif species_upper in ['NO','NITROGEN OXIDE']:
            changed_name = 'NO'
        # If none of these then set to None
        else:
            changed_name = None

        if changed_name in self.availble_species:
            self.species_name = changed_name
        else:
            print "%s not availble. \nAvaible species for limits are: %s" % (species_input,self.availble_species)
            self.species_name = None
        return self

    def get_limits(self):
        """
            Get the availble limits for the given species.
        """
        # Check the species name given by the user
        self.check_species_name(self.input_species)
        species = self.species_name
        # If its not avaible return None
        if not species:
            return None
        else:
            # Get the full database then select only species of interest
            df = self.full_database
            species_df = df.loc[species]
            # Remove any data that is NaNs (ie no available limits)
            species_df.dropna(inplace = True)

            # Get limit types. Loop through all info. If its not a unit
            # or a per year exceedance then its a AQ limit (hopefully).
            limit_types = []
            for i in species_df.index:
                if i.split('.')[0] not in ['UNIT', 'PER_YEAR']:
                    limit_types.append(i)

            # Loop throuh the limit types and put the relevant info into a dictionary
            limit_type_dict = {}
            for n, lt in enumerate(species_df.index):
                if lt in limit_types:
                    # Get the information from the DataFrame
                    species_name = 'Test species' #species
                    limit = species_df[lt]
                    unit = species_df.UNIT
                    limit_name = lt.replace('_', ' ')
                    # Get the exceedance value that the DataFrame column one past the limit type
                    # Try and see if there is an exceedance in the DataFrame
                    # If not then set to None
                    try:
                        exceedance = '%d per year' % int(species_df[species_df.index[n + 1]])
                    except KeyError:
                        exceedance = 'None'
                    except IndexError:
                        exceedance = 'None'

                    # Set all the variables into a class thats in a named dictionary
                    limit_type_dict[lt] = split_limits(species_name,limit, unit,
                        limit_name, exceedance)

            self.limit_type = limit_type_dict

        return self

class split_limits(object):
    """
        A simple class that assigns class variables. This is used in the AQ_limits
        class. Input needed:
            species_name - The name of the species
            limit - The limit given for this species
            unit - The unit of the limit (eg. ugm-3)
            limit_name - The name of this limit (eg. UK Daily, EU 8HOURLY)
            exceedance - How many times this should not be exceeded per year
                (This is not availble for all species and will be set to None if
                not availble.)
    """

    def __init__(self, species_name, limit, unit, limit_name, exceedance = None):
        super(split_limits, self).__init__()
        self.species_name =species_name
        self.limit = limit
        self.unit = unit
        self.limit_name = limit_name
        self.exceedance = exceedance


## ============================================================================
## END OF PROGAM
## ============================================================================
