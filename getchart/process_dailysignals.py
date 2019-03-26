import os
import csv
import datetime
import sys
sys.path.insert(0, '..')
import config
import utils

table=[]
header=[]

localconfig=config.config['PROCESS']
date=''
if localconfig['date'] == "all":
    # NOT IMPLEMENTED YET
    import sys
    sys.exit()
elif localconfig['date'] == "latest":
    # NOT IMPLEMENTED YET
    import sys
    sys.exit()
else:
    date=localconfig['date']
inputdir = utils.getroot()+config.config['EXTERNAL']['localfolder'] + date
ofile = inputdir+'.csv'
if localconfig['file'] != "filename":
    ofile=localconfig['file']

# header is split like this to make it easier for me to move the most important stuff to front
header= ["Date","Index"]
header=header+["emaRatio","emaBSRatio","BuySellRatio"]
header=header+["buy","sell","preBuy","preSell", "HiLer","Cler","TrapBuySum","TrapSellSum","TrapRatio","AboveEMA","BelowEMA", "EMABuy","EMASell","Sureness"]

# get list of files within input directory
listfiles=os.listdir(inputdir)

# data
#  stocks within index (Stock, date, ...)
#  data to grab (AboveEMA,emaRatio,EMABuy, EMASell, BSR, Sureness)
#  some random information (AI-1, -2 to 2 ...) to NOT grab

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
            # this is also an entry we might need
            row2=row[0].split(":")
            data.update(dict(zip(row2[::2], row2[1::2])))

    # save data
    entry.append(datetime.datetime.strptime(date, '%Y%m%d').strftime('%m/%d/%Y'))
    entry.append(file[:-4])
    for column in header[2:]:
        entry.append(data[column])
    table.append(entry)

# save file
utils.savetable(header,table,ofile)
