#!/usr/bin/env python
#
# Site creation. Preparation XML files based on template
# version 0 Varmioz Draft
# format of command is >python xml_gen_v.0.py xml_input.csv

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
    '''take xml and add trail
    '''
    with open(filename, 'a') as target_xml:
        target_xml.write('</cmData>' + '\n' 
        + '</raml>' + '\n') 

def handle_data(data):
    ''' function which is doing data processing itself
    '''
    if not os.path.isfile(data):   # Return True if path of csv file is an existing directory.
        print 'Error! CSV data file does not exists: %s' % data
        sys.exit('Or type correct filename <csv_data>') # exit the process when called from the main thread with message in ('')
        
    with open(data, 'rb') as csvfile:
        
        reader = csv.DictReader(csvfile)	# class csv.DictReader(csvfile, fieldnames=None, restkey=None, restval=None, dialect='excel', *args, **kwds)
        filename = raw_input('Enter the target XML filename without extension: ') + '.xml' # ask user to enter target xml filename

        while os.path.isfile(filename): # checking for unic targetxml name
            filename = raw_input('Target XML already exist, please enter new one: ') + '.xml'
        
        t = time.clock()    # takes current time
        xml_header(filename) # add nsn_xml header

        for row in reader:	# go though all line in CSV

            template_name = row['TemplateName']	# take template_name from line in column 'TemplateName'
            
            if template_name in templates:  # check is template is in dictionary of used ones to not re-check path of template
                template = templates[template_name] # takes template from dictionary

            elif os.path.isfile(template_name):	# Check if template_name has corresponding template.ept is in working directory.
                template = open(template_name, 'r').read()	# The method read() reads at most size bytes from the tepmlate.ept file and put it in variable template
                templates[template_name] = template    # Put unused before template to dictionary

            else:
                print 'Error! Template `%s` does not exist' % template_name
                sys.exit('WTF?')

            with open(filename, 'a') as target_xml:    # take empty xml to append data
                target_xml.write(template.format(**row))    # substitute key values in template with values from row

        xml_trailer(filename) # add nsn_xml trailer

    print 'File %s generated for %s seconds' % (filename, (time.clock() - t))    # N files for x sec
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' run by ' + sys.platform    # systime + platform identifier

if __name__ == '__main__':

    if len(sys.argv) <> 2: # to check if command format is right and contains 2 arguments after script_name
		sys.exit('Type command in format ./pabis-over-eth.py <csv_data>')  # exit the process when called from the main thread with message in ('')
    
    handle_data(sys.argv[1]) # handle csv filename
