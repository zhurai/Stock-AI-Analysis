import csv
import utils
import config

table = []
header = []

localconfig=config.config['TEST']
file=config.config['INPUT']['tfile']
ofile='output\\' + utils.getfilename() + '.csv'
if localconfig['file'] != "filename":
    ofile=localconfig['file']

table = utils.readtable(file)
header = utils.readheaders(file)
header = utils.appendheaders(header,["Cash","Shares","Balance","Stop","Action","Trades","Holding Days","Profit"])

# Date,Open,High,Low,Close,Volume,5-EMA,BuySellRatio,Sureness,Signal,Low3, High3, Cash, Shares, Balance, Stop
#   0 , 1  , 2  , 3 , 4   ,  5   , 6   ,     7      ,   8    , 9    , 10,  11   ,  12,  13    ,  14    ,  15 

cash=10000
shares=0
balance=10000
stop=0
action=''
trades=0
holdingdays=0
profit=0

'''
Profit()=Balance()-Prv_balance
Days=action_days;
Prv_balance=0;
action_days=0;
stop=0

...

action_days=action_days+1

...

when you start a transaction:
action_days=0
Prv_balance=Balance()
'''

for index,row in enumerate(table):
    # initialize
    date,priceopen,pricehigh,pricelow,priceclose,pricevolume,priceema,buysellratio,sureness,signal,low3,high3 = row
    priceopen=float(priceopen)
    pricehigh=float(pricehigh)
    pricelow=float(pricelow)
    priceclose=float(priceclose)
    pricevolume=float(pricevolume)
    priceema=float(priceema)
    buysellratio=float(buysellratio)
    sureness=float(sureness)
    low3=float(low3)
    high3=float(high3)

    #print("DEBUG: ",index,date,signal,table[index-1][9],end=' ')

    if index == 0:
        # do nothing
        # <N>
        action=action+''
        None
    else:
        
        if table[index-1][9] == "NEUTRAL":
            # do nothing
            # <N>
            action=action+''
            days=days+1
            None
        elif table[index-1][9] == "BUY":
            if shares <0:
                # previously short
                # buy shares to cover short AND buy additional shares
                # <SL>
                action=action+'SL'
                shares=(cash+shares*priceopen)/priceopen
                cash=0
                if localconfig.getboolean('stop'):
                    stop=low3
                trades=trades+1
            elif shares > 0:
                # previously long
                # fix stop
                # <>
                action=action+''
                if localconfig.getint('stop_type') == 1 and localconfig.getboolean('stop'):
                    stop=low3
            elif shares == 0:
                # previously neutral
                # buy shares
                # <NL>
                action=action+'NL'
                shares=balance/priceopen
                cash=0
                if localconfig.getboolean('stop'):
                    stop=low3
                trades=trades+1
            #print ("TYPE3",end=' ')
        elif table[index-1][9] == "SELL":
            if shares == 0:
                # previously no position/neutral
                # short
                # <NS>
                action=action+'NS'
                shares=-1*(balance/priceopen)
                cash=balance-shares*priceopen
                if localconfig.getboolean('stop'):
                    stop=high3
                trades=trades+1
            elif shares < 0:
                # previously short
                # fix stop
                # <>
                action=action+''
                if localconfig.getint('stop_type') == 1 and localconfig.getboolean('stop'):
                    stop=high3
            elif shares > 0:
                # previously long
                # sell shares, then short
                # LS
                action=action+'LS'
                cash=shares*priceopen*2
                shares=-1*shares
                if localconfig.getboolean('stop'):
                    stop=high3
                trades=trades+1
            #print ("TYPE4",end=' ')
                
        if shares < 0 and pricehigh > stop and localconfig.getboolean('stop'):
            # stopped out
            # +T
            if 'S' in action:
                action=action+'T'
            else:
                action=action+'ST'
            cash = cash+stop*shares
            shares=0
            stop=0
            #print ("TYPE1",end=' ')
            trades=trades+1
        elif shares > 0 and pricelow < stop and localconfig.getboolean('stop'):
            # stopped out
            # +T
            if 'L' in action:
                action=action+'T'
            else:
                action=action+'LT'
            cash = stop*shares
            shares=0
            stop=0
            #print ("TYPE2",end=' ')
            trades=trades+1

            
    balance=cash+shares*priceclose
    
    #print (cash,shares,balance,stop, end=' ')
    
    row.append(str(cash))
    row.append(str(shares))
    row.append(str(balance))
    row.append(str(stop))
    row.append(str(action))
    row.append(str(trades))
    row.append(str(holdingdays))
    row.append(str(profit))

    action=''
    trades=0
    #print(" ")



# save file
utils.savetable(header,table,ofile)

# DEBUG
#utils.outputtable(table)

