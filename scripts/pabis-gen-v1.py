#!/usr/bin/env python
#
#   Packet Abis over Ethernet. Preparation XML files based on template
#   version 1 Гыщм
#   format of command is >python pabis-over-eth-v4.py PAbis_BTS_input.csv


import os	# Miscellaneous operating system interfaces
import sys	# System-specific parameters and functions
import csv	# CSV File Reading and Writing

templates = {} # create dictionary with used templates

def handle_data(data):
    ''' function which is doing data processing itself
    '''
    if not os.path.isfile(data):   # Return True if path of csv file is an existing directory.
        print 'Error! CSV data file does not exists: %s' % data
        sys.exit('Or type correct filename <csv_data>')		# exit the process when called from the main thread with message in ('')
        
    with open(data, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)	# class csv.DictReader(csvfile, fieldnames=None, restkey=None, restval=None, dialect='excel', *args, **kwds)
        
        for row in reader:	# go though all line in CSV
            template_name = row['TemplateName']	# take template_name from line in column 'TemplateName'
              
            if os.path.isfile(template_name):	# Check if template_name has corresponding template.ept is in working directory.
                template = open(template_name, 'r').read()	# The method read() reads at most size bytes from the tepmlate.ept file and put it in variable template
                                
            else:
                print 'Error! Template `%s` does not exist' % template_name
                sys.exit()

            print template_name, row['filename']   # print template_name with target .ept
            with open(row['filename'], 'wb') as target_ept:   # take empty target.ept
                target_ept.write(template.format(**row))
    print sys.platform   # platform identifier
if __name__ == '__main__':

    if len(sys.argv) <> 2: # to check if command format is right and contains 2 arguments after script_name
		sys.exit('Type command in format ./pabis-over-eth.py <csv_data>')  # exit the process when called from the main thread with message in ('')
    
    handle_data(sys.argv[1]) # handle csv filename
