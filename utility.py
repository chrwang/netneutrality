# Import libraries

import os
import csv

def view_help(): 
    '''
    This method reads content from the help file to 
    the command prompt. 
    '''
    with open('help.txt', 'r') as f: 
        content = f.read()
    return content

def view_redirect(): 
    '''
    This method prints the current list of sites that are being 
    redirected and the destinations of the redirects to the 
    command prompt.  
    '''
    pass

def view_block():
    '''
    This method prints the current list of sites that are being 
    blocked to the command prompt. 
    '''
    f = open('blocked_sites', 'r') 

def view_throttle(): 
    '''
    This method prints the current list of sites that are being 
    throttled to the command prompt. 
    '''
    with open('throttle_list', 'r') as f: 
        all_lines = f.readlines()
    print(all_lines)

def read_list(): 
    '''
    This method returns the content of a desinated list. 
    '''
    with open('dns_list_test') as f: 
        reader = csv.DictReader(f)
