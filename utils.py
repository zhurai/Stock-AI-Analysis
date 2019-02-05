# for various functions to use
import csv

# READ IN TABLE
# file = input file
def readtable(file):
    table=[]

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
    return table

# DEBUG FUNCTION
# Table = memory table
def outputtable (table):
    print('\n'.join(map(' '.join, table)))

# READ IN HEADERS
# file = input file
def readheaders(file):
    header = []
    with open(file) as csvfile:
        csvreader = csv.reader(csvfile,delimiter=',')
        linecount=0
        for row in csvreader:
            if linecount == 0:
                # labels
                header=row
                linecount+=1
    return header

# APPEND HEADERS
# header = list of all headers
# append = list of entries to append
def appendheaders(header,append):
    for entry in append:
        header.append(entry)
    return header

# OUTPUT FILE
# headers = list of all headers
# table = to be written to table
# file = output file
def savetable(header,table,file):
    with open(file,mode='w',newline='') as csvfile:
        write=csv.writer(csvfile,delimiter=',')
        write.writerow(header)
        for row in table:
            write.writerow(row)
