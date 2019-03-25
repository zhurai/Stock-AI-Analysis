import sys
sys.path.insert(0, '..')
import utils
import config
sys.path.insert(0, '../analysis')
sys.path.insert(0, '../backtest')

# override default ANALYSIS settings
config.config['ANALYSIS']['days']='3'
config.config['ANALYSIS']['highlowinclusive']='false'
config.config['ANALYSIS']['signal_type']='1'

import analysis
#analysis.main()

# override default TEST settings
config.config['TEST']['stop']='true'
config.config['TEST']['stop_type']='0'

import test
#test.main()


