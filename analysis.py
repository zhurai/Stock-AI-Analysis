import csv
import utils
import config

table=[]
file=r"input\analysis.csv"
#file=r"input\analysis2.csv" # testfile
ofile=r"output\analysis_output.csv"
header = []

table = utils.readtable(file)
header = utils.readheaders(file)
header = utils.appendheaders(header,["Signal","Low "+str(config.days),"High "+str(config.days)])

# Date,Open,High,Low,Close,Volume,5-EMA,BuySellRatio,Sureness
#   0 , 1  , 2  , 3 , 4   ,  5   , 6   ,     7      ,   8
# Buy Signal = BuySellRatio > 1 && Sureness > 0.5 && Close > 5-EMA
# Sell Signal = BuySellRatio < 1 && Sureness > 0.5 && Close < 5-EMA

for index,row in enumerate(table):
    # initialize
    date,priceopen,pricehigh,pricelow,priceclose,pricevolume,priceema,buysellratio,sureness = row
    priceopen=float(priceopen)
    pricehigh=float(pricehigh)
    pricelow=float(pricelow)
    priceclose=float(priceclose)
    pricevolume=float(pricevolume)
    priceema=float(priceema)
    buysellratio=float(buysellratio)
    sureness=float(sureness)

    issure=0
    isbuy=0
    issell=0

    # debug
    #print(date + " ",end='')

    #### SIGNALS
    '''
    # sureness
    if sureness > 0.5:
        issure=1
    else:
        issure=0
    # if buy signal
    if issure==1 and buysellratio > 0.0 and priceclose > priceema:
        isbuy=1
        #print ("buy signal ",end='')
        row.append("BUY")
    # if sell signal
    elif issure==1 and buysellratio < 0.0 and priceclose < priceema:
        issell=1
        #print ("sell signal ",end='')
        row.append("SELL")
    # if neutral signal
    else:
        #print ("no signal ",end='')
        row.append("NEUTRAL")
    #print("")

    # ALT
    '''
    # if buy signal
    if buysellratio > 0.0:
        isbuy=1
        #print ("buy signal ",end='')
        row.append("BUY")
    # if sell signal
    elif buysellratio < 0.0:
        issell=1
        #print ("sell signal ",end='')
        row.append("SELL")
    # if neutral signal
    else:
        #print ("no signal ",end='')
        row.append("NEUTRAL")
    
    
    #### STOP PRICES
    # min=longstop
    # max=shortstop
    # min= low of last 3 days including today
    # max= high of last 3 days including today
    '''
    low3day = []
    high3day = []
    if index==0:
        # no other entries
        low3day= [pricelow,pricelow,pricelow]
        high3day= [pricehigh,pricehigh,pricehigh]
    elif index==1:
        # 1 other entry
        low3day = [pricelow,float(table[index-1][3]),pricelow]
        high3day = [pricehigh,float(table[index-1][2]),pricehigh]
    else:
        low3day = [pricelow,float(table[index-1][3]),float(table[index-2][3])]
        high3day = [pricehigh,float(table[index-1][2]),float(table[index-2][2])]
    '''
    lowday = []
    highday = []
    # whenever there are lower entries
    #  we are at the top of the list, can assume we can start at index0
    if index<config.days-1:
        for x in range(0,index+1):
            lowday.append(float(table[x][3]))
            highday.append(float(table[x][2]))
    # same or more index=days
    else:
        for x in range(0,config.days):
            lowday.append(float(table[index-x][3]))
            highday.append(float(table[index-x][2]))
    longstop=min(lowday)
    shortstop=max(highday)
    row.append(longstop)
    row.append(shortstop)
    
# save file
utils.savetable(header,table,ofile)
        

