#!/usr/bin/env python
#
#   SCTP logs parsing to get CSV files with all parameters of Abis SCTP associasions solid list
#	format of command is >python sctp_parsing.py

import csv

def parsing(filename):
    with open(filename,'r') as source: # search for BSC belong to sctp
        for line in source:
            line.strip() # remove spaces arround
            
            if 'SCTP ASSOCIATION ASSOC' in line: row = {} #clearing row before new assoc

            l = line.split() # split line into list of words

            if 'IUA   SERVER' in line: # parsing single associacion
                row['ASSOC_NAME'] = l[0]
                row['ASSOC_ID'] = l[1]
                row['BCSU_ID'] = (l[2])[5]
                row['PARAM_SET'] = l[5]
                row['STATE'] = l[6]
            elif 'SOURCE ADDRESS 1' in line:
                row['SOURCE_ADR'] = l[11]
            elif 'SOURCE PORT' in line:
                row['PORT'] = l[12]
            elif 'PRIMARY DEST. ADDRESS' in line:
                slash = l[8].find('/')
                row['DEST_ADR'] = l[8][0:slash]
                row['MASK'] = l[8][slash+1:]
                writer.writerow (row) # appending row to csv
				

with open('sctp_zoyv.txt') as source: # search for BSC belong to sctp and defining file name
    for line in source:
        line.strip()
        p = line.split()
        if line.startswith('mcBSC'):
            csv_name = p[1] + '_SCTP.csv'
        elif 'FlexiBSC' in line:
            csv_name = p[1] + '_SCTP.csv'
            

with open(csv_name, 'wb') as csvfile: # creating template csv
    fields = ['ASSOC_ID','ASSOC_NAME','BCSU_ID','PARAM_SET','SOURCE_ADR','DEST_ADR','MASK','PORT','STATE']
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    parsing('sctp_zoyv.txt')
	
'''
Format of parsed text is below

FlexiBSC  BSC888                    2015-02-13  15:45:48

INTERROGATING SCTP ASSOCIATION DATA

SCTP ASSOCIATION ASSOC         SCTP         PARAMETER SET
NAME             IND   UNIT    USER  ROLE   NAME             STATE
---------------- ----- ------- ----- ------ ---------------- -------------
TESTBCFTDM           0 BCSU-0  IUA   SERVER AFAST            SCTP-DOWN

    SOURCE ADDRESS 1 . . . . . . . : 10.0.1.2
    SOURCE ADDRESS 2 . . . . . . . :
    SOURCE PORT  . . . . . . . . . : 49152
    PRIMARY DEST. ADDRESS  . . . . : 10.0.2.190/26
    SECONDARY DEST. ADDRESS  . . . :
    DESTINATION PORT . . . . . . . : 49152

    MAX. DATA STREAM COUNT . . . . : 64
    SPECIFICATION VERSION  . . . . : 1
'''
