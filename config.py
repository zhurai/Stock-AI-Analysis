import configparser

# Default Values
configfile='config.ini'
debug=False
inputfile=''
gdrivekey=''
gdriverootdir=''
gdrivecsvid=''
days=0

config = configparser.ConfigParser()
config.read(configfile)

debug=config['DEBUG'].getboolean('debug')

inputfile=config['INPUT']['file']

days=int(config['ANALYSIS']['days'])

gdrivekey=config['GOOGLEAPI']['key']
gdriverootdir=config['GOOGLEAPI']['dbroot']
gdrivecsvid=config['GOOGLEAPI']['dbid']


