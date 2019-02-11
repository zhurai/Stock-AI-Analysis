import configparser

# Default Values
configfile='config.ini'
debug=False
inputfile=''
gdrivekey=''
gdriverootdir=''
gdrivecsvid=''


config = configparser.ConfigParser()
config.read(configfile)

debug=config['DEBUG'].getboolean('debug')

inputfile=config['INPUT']['file']

gdrivekey=config['GOOGLEAPI']['key']
gdriverootdir=config['GOOGLEAPI']['dbroot']
gdrivecsvid=config['GOOGLEAPI']['dbid']


