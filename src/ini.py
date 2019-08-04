'''
Parse ini file for autorun
'''

import configparser
import pandas as pd


class IniInput(object):

    def __init__(self, config_file):

        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        config_sections = self.config.sections()

        if config_sections:

            self.customers_file = self.config['GREENFIELD_INPUTS']['CUSTOMERS_FILE']
            self.customers = pd.read_csv(self.customers_file)
            self.minimum_number_of_clusters = int(self.config['GREENFIELD_INPUTS']['MINIMUM_NUMBER_OF_CLUSTERS'])
            self.maximum_number_of_clusters = int(self.config['GREENFIELD_INPUTS']['MAXIMUM_NUMBER_OF_CLUSTERS'])
            self.minimum_elements_in_a_cluster_ratio = float(self.config['GREENFIELD_INPUTS'][
                'MINIMUM_ELEMENTS_IN_A_CLUSTER_RATIO'])
            self.maximum_elements_in_a_cluster_ratio = float(self.config['GREENFIELD_INPUTS'][
                'MAXIMUM_ELEMENTS_IN_A_CLUSTER_RATIO'])

        else:
            raise ValueError('Update Ini file format')
