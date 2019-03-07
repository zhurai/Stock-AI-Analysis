import utils
import config

# override default ANALYSIS settings
config.config['ANALYSIS']['days']='3'
config.config['ANALYSIS']['highlowinclusive']='false'
config.config['ANALYSIS']['signal_original']='true'
config.config['ANALYSIS']['signal_buysellratio_only']='false'

import analysis
#analysis.main()

# override default TEST settings
config.config['TEST']['stop']='true'
config.config['TEST']['stop_type']='0'

import test
#test.main()


