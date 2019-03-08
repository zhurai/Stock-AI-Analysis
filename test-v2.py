import csv
import utils
import config

table = []
header = []

localconfig=config.config['TEST']
file=config.config['INPUT']['tfile']
ofile='output\\' + utils.getfilename() + '.csv' 
ofile2='output\\' + utils.getfilename() + '.log.csv'
if localconfig['file'] != "filename":
    ofile=localconfig['file']

table = utils.readtable(file)
header = utils.readheaders(file)
header = utils.appendheaders(header,["Cash","Shares","Balance","Stop","Trades","Action"])
header2 = ['Buy Date','Sell Date','Action','Days','Profit']
table2 = []

# Date,Open,High,Low,Close,Volume,EMA,EMAge,HiLer,Cler,TrapCode,emaRatio,BuySellRatio,emaBuySellRatio,HiLer,Cler,TrapRatio,BAR,HLBar,Sureness  || Signal,Low3, High3, Cash, Shares, Balance, Stop
#  0    1   2     3   4      5     6   7     8     9      10     11         12              13         14    15    16       17  18     19           20   21     22      23   24       25      26

cash=10000
shares=0
balance=10000
stop=0
action=''
dailyaction=''
trades=0
holdingdays=0
profit=0
balance2=0
days=0
boughtdate=''

for index,row in enumerate(table):
    # initialize
    date,priceopen,pricehigh,pricelow,priceclose,pricevolume,priceema,emaage,hiler0,cler0,trapcode,emaratio,buysellratio,emabuysellratio,hiler,cler,trapratio,bar,hlbar,sureness,signal,low3,high3 = row
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
    low3=float(low3)
    high3=float(high3)
    row2=[]

    #print("DEBUG: ",index,date,signal,table[index-1][20],end=' ')

    if index == 0:
        # do nothing
        # <N>
        action=action+''
        None
    else:
        
        if table[index-1][20] == "NEUTRAL":
            # Neutral
            # set stop
            if localconfig.getboolean('stop'):
                if localconfig.getint('stop_type') == 1:
                    if shares > 0:
                        # long
                        if priceopen < low3:
                            stop=priceopen
                        else:
                            stop=low3
                    elif shares < 0:
                        # short
                        if priceopen > high3:
                            stop=priceopen
                        else:
                            stop=high3
            
            # do nothing
            # <N>
            action=action+''
            dailyaction=dailyaction+''
            days=days+1
            holdingdays=holdingdays+1


        elif table[index-1][20] == "BUY":
            # LONG
            
            # set stop
            if localconfig.getboolean('stop'):
                if shares > 0:
                    if localconfig.getint('stop_type') == 1:
                        if priceopen < low3:
                            stop=priceopen
                        else:
                            stop=low3
                else:
                    if priceopen < low3:
                        stop=priceopen
                    else:
                        stop=low3

            
            if shares <0:
                # previously short
                # buy shares to cover short AND buy additional shares
                # <SL>
                if 'S' in action:
                    action=action+'L'
                else:
                    action=action+'SL'
                dailyaction=dailyaction+'SL'
                holdingdays=holdingdays+1
                profit=balance-balance2
                row2.append(boughtdate)
                row2.append(date)
                row2.append(str(action))
                row2.append(str(holdingdays))
                row2.append(str(profit))
                table2.append(row2)
                row2=[]
                shares=(cash+shares*priceopen)/priceopen
                cash=0

                trades=trades+1
                action=''
                balance2=balance
                boughtdate=date
                holdingdays=0
                profit=0
            elif shares > 0:
                # previously long
                # fix stop
                # <>
                action=action+''
                dailyaction=dailyaction+''
                holdingdays=holdingdays+1
            elif shares == 0:
                # previously neutral
                # buy shares
                # <NL>
                action=action+'NL'
                dailyaction=dailyaction+'NL'
                shares=balance/priceopen
                cash=0
                trades=trades+1
                balance2=balance
                boughtdate=date
            #print ("TYPE3",end=' ')
            
        elif table[index-1][20] == "SELL":
            # SHORT
            
            # set stop
            if localconfig.getboolean('stop'):
                if shares < 0:
                    if localconfig.getint('stop_type') == 1:
                        if priceopen > high3:
                            stop=priceopen
                        else:
                            stop=high3

                else:
                    if priceopen > high3:
                        stop=priceopen
                    else:
                        stop=high3



            if shares == 0:
                # previously no position/neutral
                # short
                # <NS>
                action=action+'NS'
                dailyaction=dailyaction+'NS'
                shares=-1*(balance/priceopen)
                cash=balance-shares*priceopen
                balance2=balance
                boughtdate=date
                trades=trades+1
            elif shares < 0:
                # previously short
                # fix stop
                # <>
                action=action+''
                dailyaction=dailyaction+''
                holdingdays=holdingdays+1
            elif shares > 0:
                # previously long
                # sell shares, then short
                # LS
                if 'L' in action:
                    action=action+'S'
                else:
                    action=action+'LS'
                dailyaction=dailyaction+'LS'
                holdingdays=holdingdays+1
                profit=balance-balance2
                row2.append(boughtdate)
                row2.append(date)
                row2.append(str(action))
                row2.append(str(holdingdays))
                row2.append(str(profit))
                table2.append(row2)
                row2=[]
                
                cash=shares*priceopen*2
                shares=-1*shares
                trades=trades+1
                action=''
                holdingdays=0
                profit=0
                balance2=balance
                boughtdate=date
            #print ("TYPE4",end=' ')

        # Check if Stopped Out
        if shares < 0 and pricehigh > stop and localconfig.getboolean('stop'):
            # stopped out
            # +T
            if 'S' in action:
                action=action+'T'
            else:
                action=action+'ST'
            if 'S' in dailyaction:
                dailyaction=dailyaction+'T'
            else:
                dailyaction=dailyaction+'ST'
            cash = cash+stop*shares
            shares=0
            stop=0
            profit=balance-balance2
            #print ("TYPE1",end=' ')
            trades=trades+1
            row2.append(boughtdate)
            row2.append(date)
            row2.append(str(action))
            row2.append(str(holdingdays))
            row2.append(str(profit))
            table2.append(row2)
            row2=[]
            action=''
            holdingdays=0
            profit=0
        elif shares > 0 and pricelow < stop and localconfig.getboolean('stop'):
            # stopped out
            # +T
            if 'L' in action:
                action=action+'T'
            else:
                action=action+'LT'
            if 'L' in dailyaction:
                dailyaction=dailyaction+'T'
            else:
                dailyaction=dailyaction+'LT'
            cash = stop*shares
            shares=0
            stop=0
            profit=balance-balance2
            #print ("TYPE2",end=' ')
            trades=trades+1
            row2.append(boughtdate)
            row2.append(date)
            row2.append(str(action))
            row2.append(str(holdingdays))
            row2.append(str(profit))
            table2.append(row2)
            row2=[]
            action=''
            holdingdays=0
            profit=0

            
    balance=cash+shares*priceclose
    
    #print (cash,shares,balance,stop, end=' ')
    
    row.append(str(cash))
    row.append(str(shares))
    row.append(str(balance))
    row.append(str(stop))
    row.append(str(trades))
    row.append(str(dailyaction))
    dailyaction=''
    
    #action=''
    trades=0
    #print(" ")



# save file
utils.savetable(header,table,ofile)

# save file 2
utils.savetable(header2,table2,ofile2)

# DEBUG
#utils.outputtable(table)
#utils.outputtable(table2)
