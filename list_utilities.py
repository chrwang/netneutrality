# Import libraries

import os
import csv

def add_to_list(url, flag, dest, delay):
    '''
    This method adds a new row of data to the dns_list 
    file given inputs of field values. 
    '''
    delete_from_list(url)
    fields = [url, flag, dest, delay]
    with open('dns_list', 'a') as f: 
        writer = csv.writer(f)
        writer.writerow(fields)

def add_to_block(site_target): 
    '''
    This method adds a new row of data to the dns_list 
    file with the url of a designated site to be blocked 
    by this throttling application. 
    '''
    add_to_list(site_target, 'BLOC', '', '')

def add_to_redirect(site_target, site_dest): 
    '''
    This method adds a new row of data to the dns_list file 
    with the url of a designated site to be redirected and 
    the url/ip address of the destination of the redirect. 
    '''
    add_to_list(site_target, 'RDIR', site_dest, '')

def add_to_throttle(site_target, delay_time): 
    '''
    This method adds a new row of data to the dns_list file 
    with the url of a designated site to be throttled and 
    the amount of delay for the site. 
    '''
    add_to_list(site_target, 'THR', '', delay_time)

def view_help(): 
    '''
    This method reads content from the help file to 
    the command prompt. 
    '''
    with open('help.txt', 'r') as f: 
        content = f.read()
    return content

def view_block():
    '''
    This method returns the current list of sites that are being
    blocked to the command prompt.
    '''
    blocked_sites = []
    with open('dns_list') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['type'] == 'BLOC':
                blocked_sites.append(row['url'])

    return blocked_sites
    
def view_redirect(): 
    '''
    This method returns the current list of sites that are being 
    redirected and the destinations of the redirects to the 
    command prompt.  
    '''
    site_target = []
    site_dest = []
    with open('dns_list') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['type'] == 'RDIR': 
                site_target.append(row['url'])
                site_dest.append(row['dest'])
    return site_target, site_dest

def view_throttle(): 
    '''
    This method returns the current list of sites that are being 
    throttled to the command prompt. 
    '''
    site_target = []
    site_delay = []
    with open('dns_list') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['type'] == 'THR':
                site_target.append(row['url'])
                site_delay.append(row['delay'])
    return site_target, site_delay

def delete_from_list(url):
    '''
    This method deletes a designated line from the list of sites. 
    If no match is found, nothing is deleted. 
    '''
    with open('dns_list', 'r') as f: 
        data = list(csv.reader(f))

    with open('dns_list', 'w') as f: 
        writer = csv.writer(f)
        for row in data: 
            if row[0] == url: 
                pass
            else: 
                writer.writerow(row)

