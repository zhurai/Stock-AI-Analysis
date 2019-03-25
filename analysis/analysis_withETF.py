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

def import_tables(table,newfile):
    index1 = 0
    for row1 in table[:]:
        tabledate=row1[0]
        datefound=-1
        data=[]
        for index2,row2 in enumerate(utils.readtable(newfile)):
            # Date, Open, High, Low, Close, Adj Close, Volume
            readdate=row2[0]
            readopen=row2[1]
            readhigh=row2[2]
            readlow=row2[3]
            readclose=row2[4]
            readadjclose=row2[5]
            readvolume=row2[5]

            # fix the spxldate to be similar format
            # windows specific
            readdate=time.strftime("%#m/%#d/%Y",time.strptime(readdate,"%Y-%m-%d"))
            
            # compare tabledate with spxldate
            if row1[0] == readdate:
                datefound = 1
                data.append(readopen)
                data.append(readhigh)
                data.append(readlow)
                data.append(readclose)
        
        if datefound != 1:
            # delete row
            table.remove(row1)
        else:
            # add the information
            row1.append(data[0])
            row1.append(data[1])
            row1.append(data[2])
            row1.append(data[3])
        datefound=-1
    index1+=1

import_tables(table,spxlfile)
import_tables(table,spxsfile)

# Date,Open,High,Low,Close,Volume,EMA,EMAge,HiLer,Cler,TrapCode,emaRatio,BuySellRatio,emaBuySellRatio,HiLer,Cler,TrapRatio,BAR,HLBar,Sureness,SPXL-Open,SPXL-High,SPXL-Low,SPXL-Close,SPXS-Open,SPXS-High,SPXS-Low,SPXS-Close
#  0    1   2     3   4      5     6   7     8     9      10     11         12              13         14    15    16       17  18     19        20        21       22         23         24       25         26      27


for index,row in enumerate(table):
    # initialize
    date=row[0]
    priceopen=float(row[1])
    pricehigh=float(row[2])
    pricelow=float(row[3])
    priceclose=float(row[4])
    pricevolume=float(row[5])
    priceema=float(row[6])
    emaage=float(row[7])
    hiler=float(row[8])
    cler=float(row[9])
    trapcode=float(row[10])
    emaratio=float(row[11])
    buysellratio=float(row[12])
    emabuysellratio=float(row[13])
    cwhiler=float(row[14])
    cwcler=float(row[15])
    trapratio=float(row[16])
    bar=float(row[17])
    hlbar=float(row[18])
    sureness=float(row[19])

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

# save file
utils.savetable(header,table,ofile)
        

