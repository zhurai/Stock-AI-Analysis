import requests
import config
import utils
import datetime

today=datetime.datetime.combine(datetime.date.today(),datetime.datetime.min.time())

date1=1225872000
date2=today.timestamp()

#https://query1.finance.yahoo.com/v7/finance/download/SPXL?period1=1225872000&period2=1553238000&interval=1d&events=history&crumb=Wp35b.GBLT4
