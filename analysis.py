import csv

table=[]
file=r"C:\Personal\Development\Trading\analysis.csv"
#file=r"C:\Personal\Development\Trading\analysis2.csv"
ofile=r"C:\Personal\Development\Trading\output.csv"
header = []

with open(file) as csvfile:
    csvreader = csv.reader(csvfile,delimiter=',')
    linecount=0
    for row in csvreader:
        if linecount == 0:
            # labels
            header=row
            linecount+=1
        else:
            table.append(row)
            linecount+=1

# debug to print the whole table
# print('\n'.join(map(' '.join, table)))
# print(table[0][0] = 1/3/2000)


# Date,Open,High,Low,Close,Volume,5-EMA,BuySellRatio,Sureness
#   0 , 1  , 2  , 3 , 4   ,  5   , 6   ,     7      ,   8
# Buy Signal = BuySellRatio > 1 && Sureness > 0.5 && Close > 5-EMA
# Sell Signal = BuySellRatio < 1 && Sureness > 0.5 && Close < 5-EMA

for row in table:
    # initialize
    date,priceopen,pricehigh,pricelow,priceclose,pricevolume,priceema,buysellratio,sureness = row
    priceopen=float(priceopen)
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


# save file
header.append("Signal")
with open(ofile,mode='w',newline='') as csvfile:
    write=csv.writer(csvfile,delimiter=',')
    write.writerow(header)
    for row in table:
        write.writerow(row)
        
