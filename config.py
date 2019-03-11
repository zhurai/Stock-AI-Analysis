import configparser
import utils

# Default Values
configfile='config.ini'

config = configparser.ConfigParser()
config.read(configfile)
