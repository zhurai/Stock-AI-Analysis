import csv
import utils
import config

file=r"output\analysis_output.csv" # testfile
ofile=r"output\papertrade-shortonly_output.csv"
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

    if shares < 0 and pricehigh > stop:
        # stopped out
        cash = cash+stop*shares
        shares=0
        stop=0
        #print ("TYPE1",end=' ')
    elif table[index-1][9] == "NEUTRAL":
        # do nothing
        #print ("TYPE2",end=' ')
        None
    elif table[index-1][9] == "BUY" and shares<0:
        cash=cash+shares*priceopen
        shares=0
        stop=0
        #print ("TYPE3",end=' ')
    elif table[index-1][9] == "BUY" and shares>=0:
        # do nothing
        #print ("TYPE4",end=' ')
        None
    elif table[index-1][9] == "SELL" and shares==0:
        # previously no position, Short
        shares=-1*balance/priceopen
        cash=balance-shares*priceopen
        stop=high3
        #print ("TYPE5",end=' ')
    elif table[index-1][9] == "SELL" and shares>0:
        # not possible, do nothing
        #print ("TYPE6",end=' ')
        None

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

