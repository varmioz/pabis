#!/usr/bin/env python
#
#   Packet Abis over Ethernet. Preparation XML files based on template
#   version 5 Dima with dictionary to reduce processing time
#	format of command is >python pabis-over-eth-v5.py PAbis_BTS_input.csv

import os	# Miscellaneous operating system interfaces
import sys	# System-specific parameters and functions
import csv	# CSV File Reading and Writing
import time    # Time access and conversions

templates = {} # create dictionary with used templates

def handle_data(data):
    ''' function which is doing data processing itself
    '''
    if not os.path.isfile(data):   # Return True if path of csv file is an existing directory.
        print 'Error! CSV data file does not exists: %s' % data
        sys.exit('Or type correct filename <csv_data>') # exit the process when called from the main thread with message in ('')
        
    with open(data, 'rb') as csvfile:
        
        reader = csv.DictReader(csvfile)	# class csv.DictReader(csvfile, fieldnames=None, restkey=None, restval=None, dialect='excel', *args, **kwds)
        number_of_files = 0 # variable to count number of files
    
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

            number_of_files += 1
            print template_name, row['filename']   # print template_name with target .ept
            with open(row['filename'], 'wb') as target_ept:   # take empty target.ept
                target_ept.write(template.format(**row))    # substitute key values in template with values from row

    print '%i files generated for %s seconds' % (number_of_files, (time.clock() - t))    # N files for x sec
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' run by ' + sys.platform    # systime + platform identifier

if __name__ == '__main__':
	
    t = time.clock()    # takes current time
    if len(sys.argv) <> 2: # to check if command format is right and contains 2 arguments after script_name
		sys.exit('Type command in format ./pabis-over-eth.py <csv_data>')  # exit the process when called from the main thread with message in ('')
    
    handle_data(sys.argv[1]) # handle csv filename

