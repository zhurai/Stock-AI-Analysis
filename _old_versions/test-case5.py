import csv
import utils
import config

# long and short

file=r"output\analysis_output.csv" # testfile
ofile=r"output\testcase5.csv"
table=[]
header = []

table = utils.readtable(file)
header = utils.readheaders(file)
header = utils.appendheaders(header,["Cash","Shares","Balance","Stop"])

# Date,Open,High,Low,Close,Volume,5-EMA,BuySellRatio,Sureness,Signal,Low3, High3, Cash, Shares, Balance, Stop
#   0 , 1  , 2  , 3 , 4   ,  5   , 6   ,     7      ,   8    , 9    , 10,  11   ,  12,  13    ,  14    ,  15 

cash=10000
shares=0
balance=10000
stop=0

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
        None
    else:
        if table[index-1][9] == "NEUTRAL":
            # do nothing
            None
        elif table[index-1][9] == "BUY":
            if shares <0:
                # previously short
                # buy shares to cover short AND buy additional shares
                shares=(cash+shares*priceopen)/priceopen
                cash=0
                stop=low3
            elif shares > 0:
                # previously long
                # No action
                None
            elif shares == 0:
                # previously neutral
                # buy shares
                shares=balance/priceopen
                cash=0
                stop=low3
            #print ("TYPE3",end=' ')
        elif table[index-1][9] == "SELL":
            if shares == 0:
                # previously no position/neutral
                # short
                shares=-1*(balance/priceopen)
                cash=balance-shares*priceopen
                stop=high3
            elif shares < 0:
                # previously short
                # No action
                None
            elif shares > 0:
                # previously long
                # sell shares, then short
                cash=shares*priceopen*2
                shares=-1*shares
                stop=high3
            #print ("TYPE4",end=' ')

        if shares < 0 and pricehigh > stop:
            # stopped out, short case
            cash = cash+stop*shares
            shares=0
            stop=0
            #print ("TYPE1",end=' ')
        elif shares > 0 and pricelow < stop:
            # stopped out, short case
            cash = stop*shares
            shares=0
            stop=0
            #print ("TYPE2",end=' ')

    balance=cash+shares*priceclose
    
    #print (cash,shares,balance,stop, end=' ')
    
    row.append(str(cash))
    row.append(str(shares))
    row.append(str(balance))
    row.append(str(stop))
    #print(" ")



# save file
utils.savetable(header,table,ofile)

# DEBUG
#utils.outputtable(table)

