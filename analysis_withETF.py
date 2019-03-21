import csv
import utils
import config
import time

table = []
header = []

localconfig=config.config['ANALYSIS']
file=config.config['INPUT']['file']
spxsfile='input/SPXS.csv'
spxlfile='input/SPXL.csv'
ofile=config.config['INPUT']['tfile']
if localconfig['file'] != "filename":
    ofile=localconfig['file']
days=localconfig.getint('days')

table = utils.readtable(file)
header = utils.readheaders(file)
header = utils.appendheaders(header,["SPXL-Open","SPXL-High","SPXL-Low","SPXL-Close","SPXS-Open","SPXS-High","SPXS-Low","SPXS-Close"])
header = utils.appendheaders(header,["Signal","Low "+str(days),"High "+str(days)])

# Date,Open,High,Low,Close,Volume,EMA,EMAge,HiLer,Cler,TrapCode,emaRatio,BuySellRatio,emaBuySellRatio,HiLer,Cler,TrapRatio,BAR,HLBar,Sureness 
#  0    1   2     3   4      5     6   7     8     9      10     11         12              13         14    15    16       17  18     19

# import SPXL
for index1,row1 in enumerate(table):
    tabledate=row1[0]
    datefound=-1
    spxldata=[]
    for index2,row2 in enumerate(utils.readtable(spxlfile)):
        # Date, Open, High, Low, Close, Adj Close, Volume
        spxldate=row2[0]
        spxlopen=row2[1]
        spxlhigh=row2[2]
        spxllow=row2[3]
        spxlclose=row2[4]
        spxladjclose=row2[5]
        spxlvolume=row2[5]

        # fix the spxldate to be similar format
        # windows specific
        spxldate=time.strftime("%#m/%#d/%Y",time.strptime(spxldate,"%Y-%m-%d"))
        
        # compare tabledate with spxldate
        if row1[0] == spxldate:
            datefound = 1
            spxldata.append(spxlopen)
            spxldata.append(spxlhigh)
            spxldata.append(spxllow)
            spxldata.append(spxlclose)
    
    if datefound != 1:
        # delete row
        del table[index1]
    else:
        # add the information
        #print(index1)
        row1.append(spxldata[0])
        row1.append(spxldata[1])
        row1.append(spxldata[2])
        row1.append(spxldata[3])
    datefound=-1

    CHANGE TO WHILE LOOP

'''
# import SPXS
for row1 in table:
    for row2 in utils.readtable(spxsfile):
        # Date, Open, High, Low, Close, Adj Close, Volume
        None
'''

'''
for index,row in enumerate(table):
    # initialize
    date,priceopen,pricehigh,pricelow,priceclose,pricevolume,priceema,emaage,hiler0,cler0,trapcode,emaratio,buysellratio,emabuysellratio,hiler,cler,trapratio,bar,hlbar,sureness, spxlopen, spxlhigh, spxllow, spxlclose = row
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
    if localconfig.getint('signal_type') == 1:
        # "Original" Setup
        if sureness > 0.5:
            issure=1
        else:
            issure=0
        #  Sureness > 0.5, BSR > 0.0, Close > EMA
        if issure==1 and buysellratio > 0.0 and priceclose > priceema:
            isbuy=1
            row.append("BUY")
        #  Sureness > 0.5, BSR < 0.0, Close < EMA
        elif issure==1 and buysellratio < 0.0 and priceclose < priceema:
            issell=1
            row.append("SELL")
        else:
            row.append("NEUTRAL")
    elif localconfig.getint('signal_type') == 2:
        if buysellratio > 0.0:
            isbuy=1
            row.append("BUY")
        elif buysellratio < 0.0:
            issell=1
            row.append("SELL")
        else:
            row.append("NEUTRAL")
    elif localconfig.getint('signal_type') == 3:
        if emaratio > 0.0 and buysellratio > 0.0 and emabuysellratio > 0.0:
            isbuy=1
            row.append("BUY")
        elif emaratio < 0.0 and buysellratio < 0.0 and emabuysellratio < 0.0:
            issell=1
            row.append("SELL")
        else:
            row.append("NEUTRAL")
    else:
        # No Signal Type Loaded
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

'''

# save file
utils.savetable(header,table,ofile)
        

