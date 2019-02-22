import csv
import utils
import config

table = []
header = []

localconfig=config.config['ANALYSIS']
file=config.config['INPUT']['file']
ofile=config.config['INPUT']['tfile']
if localconfig['file'] != "filename":
    ofile=localconfig['file']
days=localconfig.getint('days')

table = utils.readtable(file)
header = utils.readheaders(file)
header = utils.appendheaders(header,["Signal","Low "+str(days),"High "+str(days)])

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
    if localconfig.getboolean('signal_original') == True:
        # Original Setup:
        if sureness > 0.5:
            issure=1
        else:
            issure=0
        #  Sureness > 0.5, BSR > 0.0, Close > EMA
        if issure==1 and buysellratio > 0.0 and priceclose > priceema:
            isbuy=1
            #print ("buy signal ",end='')
            row.append("BUY")
        #  Sureness > 0.5, BSR < 0.0, Close < EMA
        elif issure==1 and buysellratio < 0.0 and priceclose < priceema:
            issell=1
            #print ("sell signal ",end='')
            row.append("SELL")
        else:
            #print ("no signal ",end='')
            row.append("NEUTRAL")
        #print("")
    elif localconfig.getboolean('signal_buysellratio_only') == True:
        # Edited Setup: (Just BSR)
        if buysellratio > 0.0:
            isbuy=1
            #print ("buy signal ",end='')
            row.append("BUY")
        elif buysellratio < 0.0:
            issell=1
            #print ("sell signal ",end='')
            row.append("SELL")
        else:
            #print ("no signal ",end='')
            row.append("NEUTRAL")
    
    
    #### STOP PRICES
    # min=longstop
    # max=shortstop
    lowday = []
    highday = []
    
    if localconfig.getboolean('highlowinclusive') == True:
        if index < days-1:
            for x in range(0,index+1):
                lowday.append(float(table[x][3]))
                highday.append(float(table[x][2]))
        # same or more index=days
        else:
            for x in range(0,days):
                lowday.append(float(table[index-x][3]))
                highday.append(float(table[index-x][2]))
    else: # highlowinclusive=false
        if index == 0:
            # use current day
            lowday.append(pricelow)
            highday.append(pricehigh)
        elif index<days:
            for x in range(0,index):
                lowday.append(float(table[x][3]))
                highday.append(float(table[x][2]))
        else:
            for x in range(0,days):
                lowday.append(float(table[index-x-1][3]))
                highday.append(float(table[index-x-1][2]))
    
    longstop=min(lowday)
    shortstop=max(highday)
    row.append(longstop)
    row.append(shortstop)
        
# save file
utils.savetable(header,table,ofile)
        

