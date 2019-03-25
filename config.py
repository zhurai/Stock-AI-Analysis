import configparser
import utils
import os

# Default Values
basepath=os.path.dirname(os.path.realpath(__file__))+"/"
configfile=basepath+'config.ini'

config = configparser.ConfigParser()
config.read(configfile)
