import os
import csv
import datetime
import sys
sys.path.insert(0, '..')
import config
import utils

# temporarily not using config file to write a mvp
date = '20180119'
inputdir = utils.getroot()+'input/' + date
ofile = utils.getroot()+inputdir+'.csv'
header= ["Date","File","buy","sell","preBuy","preSell", "EMABuy","EMASell","EMARatio","buySellRatio","Sureness"]
table=[]

# get list of files within input directory
listfiles=os.listdir(inputdir)

# data
#  stocks within index (Stock, date, ...)
#  data to grab (AboveEMA,emaRatio,EMABuy, EMASell, BSR, Sureness)

# loop through files
for file in listfiles:
    # open file
    source=utils.readtable(inputdir+'/'+file)
    entry=[]
    data={}

    # loop through file
    for row in source:
        # find which type of row are we looking at
        if len(row) > 2:
            # ignore this row
            None
        elif len(row) == 2:
            # these are entries we need
            data.update(dict(zip(row[::2], row[1::2])))
        elif len(row) == 1:
            # this is also an entry we need
            # <= because Sureness is randomly in a single cell (Sureness:#) instead of Sureness,#
            row2=row[0].split(":")
            data.update(dict(zip(row2[::2], row2[1::2])))

    # save data
    entry.append(datetime.datetime.strptime(date, '%Y%m%d').strftime('%m/%d/%Y'))
    entry.append(file[:-4])
    entry.append(data['buy'])
    entry.append(data['sell'])
    entry.append(data['preBuy'])
    entry.append(data['preSell'])
    entry.append(data['EMABuy'])
    entry.append(data['EMASell'])
    entry.append(data['EMARatio'])
    entry.append(data['buySellRatio'])
    entry.append(data['Sureness'])
    table.append(entry)

# save file
utils.savetable(header,table,ofile)
