#!/usr/bin/env python
#
# Site creation. Preparation XML files based on template
# version 1 Varmioz to generate xml for BTS parameters changes base on BTS templates
#	format of command is >python xml_BTS_par_gen_v.0.py xml_par_input.csv

import os	# Miscellaneous operating system interfaces
import sys	# System-specific parameters and functions
import csv	# CSV File Reading and Writing
import time    # Time access and conversions

templates = {} # create dictionary with used templates

def xml_header(filename):
    '''take xml and create xml header
    '''
    with open(filename, 'a') as target_xml:    
        target_xml.write('<?xml version="1.0"?>' + '\n' 
        + '<raml xmlns="raml21.xsd" version="2.1">' + '\n' 
        + '<cmData xmlns="" type="plan" scope="changes" name="Default Plan">' + '\n' 
        + '<header>' + '\n' 
        + '<log user="gubarev" action="created" dateTime="' + time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()) 
        + '" appInfo="Python script">No description</log>' + '\n' 
        + '</header>' + '\n' )

def xml_trailer(filename):
    ''' take xml and add trail
    '''
    with open(filename, 'a') as target_xml:
        target_xml.write('</cmData>' + '\n' 
        + '</raml>' + '\n') 

def templ_name(SegName):
    ''' choosing template_name base on CellName
    '''
    if len(SegName) <> 13:
        print 'Check the format CellName %s !' % SegName
        sys.exit()

    elif SegName[0:3] == 'KHA' and SegName[12] == 'D': return 'genSTUD.xml'        
    elif SegName[0:3] == 'KHA' and SegName[12] == 'G': return 'genSTUG.xml'        
    elif SegName[0:3] != 'KHA' and SegName[12] == 'D': return 'genDTUD.xml'        
    elif SegName[0:3] != 'KHA' and SegName[12] == 'G': return 'genDTUG.xml'        
    else: sys.exit('Check the CellName!')

def handle_data(data):
    ''' function which is doing data processing itself
    '''
    if not os.path.isfile(data):   # Return True if path of csv file is an existing directory.
        print 'Error! CSV data file does not exists: %s' % data
        sys.exit('Or type correct filename <csv_data>') # exit the process when called from the main thread with message in ('')

    f = open('BSCId.csv','r') # open BSCId file and create dictionary BSCIds{}
    BSCIds = dict(filter(None, csv.reader(f)))
    f.close()

    with open(data, 'rb') as csvfile:
        
        reader = csv.DictReader(csvfile)	# read parameters from CSV
        filename = raw_input('Enter the target XML filename without extension: ') + '.xml' # ask user to enter target xml filename
        
        while os.path.isfile(filename): # checking for unic targetxml name
            filename = raw_input('Target XML already exist, please enter new one: ') + '.xml'
        
        t = time.clock()    # takes current time
        xml_header(filename) # add nsn_xml header
        bsnum = 0

        for row in reader:	# go though all line in CSV
            
            bsnum += 1
            template_name = templ_name(row['CellName'])	# take template_name from function processing line in column 'CellName'
                   
            if template_name in templates:  # check is template is in dictionary of used ones to not re-check path of template
                template = templates[template_name] # takes template from dictionary

            elif os.path.isfile(template_name):	# Check if template_name has corresponding template.xml in working directory.
                template = open(template_name, 'r').read()	# The method read() reads at most size bytes from the tepmlate.ept file and put it in variable template
                templates[template_name] = template    # Put unused before template to dictionary

            else:
                print 'Error! Template `%s` does not exist' % template_name
                sys.exit('WTF?')

            if int(row['TRXs']) == 1: # base on TRX quantity put parameters values in row{}
                row['amrSegLoadDepTchRateLower'] = 90
                row['amrSegLoadDepTchRateUpper'] = 100
                row['btsSpLoadDepTchRateLower'] = 90
                row['btsSpLoadDepTchRateUpper'] = 100
            elif int(row['TRXs']) == 2:
                row['amrSegLoadDepTchRateLower'] = 70
                row['amrSegLoadDepTchRateUpper'] = 90
                row['btsSpLoadDepTchRateLower'] = 70
                row['btsSpLoadDepTchRateUpper'] = 90
            else:
                row['amrSegLoadDepTchRateLower'] = 60
                row['amrSegLoadDepTchRateUpper'] = 80
                row['btsSpLoadDepTchRateLower'] = 60
                row['btsSpLoadDepTchRateUpper'] = 80

            row['CNumber'] = BSCIds[row['BSCId']] # choose corresponding CNumber
            if 'BSCId' in row: del row['BSCId'] # del unused key in row{} if exist
            
            with open(filename, 'a') as target_xml:    # take empty xml to append data
                target_xml.write(template.format(**row))    # substitute key values in template with values from row{}
                         
        xml_trailer(filename) # add nsn_xml trailer

    print "File %s generated for %s seconds with %i BTS's" % (filename, (time.clock() - t), bsnum)
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' run by ' + sys.platform # platform identifier

if __name__ == '__main__':

    if len(sys.argv) <> 2: # to check if command format is right and contains 2 arguments after script_name
		sys.exit('Type command in format ./pabis-over-eth.py <csv_data>')  # exit the process when called from the main thread with message in ('')
    
    handle_data(sys.argv[1]) # handle csv filename
