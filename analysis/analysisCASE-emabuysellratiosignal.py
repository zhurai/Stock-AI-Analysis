import csv
import sys
sys.path.insert(0, '..')
import config
import utils

table = []
header = []

localconfig=config.config['ANALYSIS']
file=utils.getroot()+config.config['INPUT']['file']
ofile=utils.getroot()+config.config['INPUT']['tfile']
if localconfig['file'] != "filename":
    ofile=localconfig['file']
days=localconfig.getint('days')

table = utils.readtable(file)
header = utils.readheaders(file)
header = utils.appendheaders(header,["Signal","Low "+str(days),"High "+str(days)])

# Date,Open,High,Low,Close,Volume,EMA,EMAge,HiLer,Cler,TrapCode,emaRatio,BuySellRatio,emaBuySellRatio,HiLer,Cler,TrapRatio,BAR,HLBar,Sureness
#  0    1   2     3   4      5     6   7     8     9      10     11         12              13         14    15    16       17  18     19

for index,row in enumerate(table):
    # initialize
    date,priceopen,pricehigh,pricelow,priceclose,pricevolume,priceema,emaage,hiler0,cler0,trapcode,emaratio,buysellratio,emabuysellratio,hiler,cler,trapratio,bar,hlbar,sureness = row
    priceopen=float(priceopen)
    pricehigh=float(pricehigh)
    pricelow=float(pricelow)
    priceclose=float(priceclose)
    pricevolume=float(pricevolume)
    priceema=float(priceema)
    emaage=float(emaage)
    hiler0=float(hiler0)
    cler0=float(cler0)
    trapcode=float(trapcode)
    emaratio=float(emaratio)
    buysellratio=float(buysellratio)
    emabuysellratio=float(emabuysellratio)
    hiler=float(hiler)
    cler=float(cler)
    trapratio=float(trapratio)
    bar=float(bar)
    hlbar=float(hlbar)
    sureness=float(sureness)

    issure=0
    isbuy=0
    issell=0

    # debug
    #print(date + " ",end='')

    #### SIGNALS
    if emabuysellratio > 0.0:
        row.append("BUY")
    elif emabuysellratio < 0.0:
        issell=1
        row.append("SELL")
    else:
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
