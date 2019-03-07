import utils
import config

# override default ANALYSIS settings
config.config['ANALYSIS']['days']='1'
config.config['ANALYSIS']['highlowinclusive']='false'
config.config['ANALYSIS']['signal_type']='2'

import analysis
#analysis.main()

# override default TEST settings
config.config['TEST']['stop']='true'
config.config['TEST']['stop_type']='1'

import test
#test.main()


