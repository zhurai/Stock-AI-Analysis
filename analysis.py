import csv
import utils

table=[]
file=r"input\analysis.csv"
#file=r"input\analysis2.csv" # testfile
ofile=r"output\analysis_output.csv"
header = []

table = utils.readtable(file)
header = utils.readheaders(file)
header = utils.appendheaders(header,["Signal","Low 3","High 3"])

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

    # sureness
    if sureness > 0.5:
        issure=1
    else:
        issure=0
    # if buy signal
    if issure==1 and buysellratio > 1.0 and priceclose > priceema:
        isbuy=1
        #print ("buy signal ",end='')
        row.append("BUY")
    # if sell signal
    elif issure==1 and buysellratio < 1.0 and priceclose < priceema:
        issell=1
        #print ("sell signal ",end='')
        row.append("SELL")
    # if neutral signal
    else:
        #print ("no signal ",end='')
        row.append("NEUTRAL")
    #print("")

    #### STOP PRICES
    # min=longstop
    # max=shortstop
    # min= low of last 3 days including today
    # max= high of last 3 days including today
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
    longstop = min(low3day)
    shortstop = max(high3day)
    row.append(longstop)
    row.append(shortstop)
    


# save file
utils.savetable(header,table,ofile)
        

