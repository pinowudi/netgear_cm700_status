import requests
from requests.auth import HTTPBasicAuth
import re
import json
import sys
from time import sleep
from config import *

def parse_upstream(inputstring):
    fieldlist = ['channel','lock_status','channel_type','channel_id','symbol_rate','frequency','power']
    upstreamlist=inputstring.split("|")
    outputdict={}
    linedict={}
    linecount=1
    fielditerator=0
    while linecount < (len(upstreamlist)-1):
        outputdict[fieldlist[fielditerator]] = upstreamlist[linecount]
        linecount = linecount + 1
        if fielditerator==(len(fieldlist)-1):
            linedict[((linecount-1)/(len(fieldlist)))]=outputdict
            outputdict={}
        fielditerator = (fielditerator + 1) % len(fieldlist)
    #print json.dumps(linedict, indent=4, sort_keys=True)
    return linedict

def parse_downstream(inputstring):
    fieldlist = ['channel','lock_status','modulation','channel_id','frequency','power','SNR','correctables','uncorrectables']
    downstreamlist=inputstring.split("|")
    outputdict={}
    linedict={}
    linecount=1
    fielditerator=0
    while linecount < (len(downstreamlist)-1):
        outputdict[fieldlist[fielditerator]] = downstreamlist[linecount]
        linecount = linecount + 1
        if fielditerator==(len(fieldlist)-1):
            linedict[((linecount-1)/(len(fieldlist)))]=outputdict
            outputdict={}
        fielditerator = (fielditerator + 1) % len(fieldlist)
    #print json.dumps(linedict, indent=4, sort_keys=True)
    return linedict

def parse_bios(inputstring):
    fieldlist = ['acquire_ds_channel_status','acquire_ds_channel_comment','connectivity_state_status','connectivity_state_comment','boot_state_status','boot_state_comment','configuration_file_status','configuration_file_comment','security_status','security_comment','current_system_time','startup_freq','provision_mode','ip_prov_mode_status','ip_prov_mode_comment','downstream_bonded_channels_partials','upstream_bonded_channels_partials']
    biosstreamlist=inputstring.split("|")
    outputdict={}
    linedict={}
    linecount=0
    fielditerator=0
    while linecount < (len(biosstreamlist)):
        outputdict[fieldlist[fielditerator]] = biosstreamlist[linecount]
        linecount = linecount + 1
        if fielditerator==(len(fieldlist)-1):
            linedict[((linecount-1)/(len(fieldlist)))]=outputdict
            outputdict={}
        fielditerator = (fielditerator + 1) % len(fieldlist)
    #print json.dumps(linedict, indent=4, sort_keys=True)
    return linedict

client = requests.Session()
r = client.get(NETGEAR_URL)
r = client.get(NETGEAR_URL, auth=(USERNAME,PASSWORD))
if r.status_code!=200:
    sys.exit("ERROR: Invalid status code %s" % r.status_code)
jsonprinter={}
valuelist = re.compile('.*var tagValueList.*')
matches = valuelist.findall(r.text)
for match in matches:
    notslash = re.compile(r'\/\/')
    if not notslash.search(match):
        pipe = re.compile(r'\|')
        if pipe.search(match):
            bios = re.compile(r'honorMdd')
            tdma = re.compile(r'TDMA')
            qam = re.compile(r'QAM')
            quote = re.compile(r'\x27(.*)\x27')
            if tdma.search(match):
                #print('Upstream: %s' % quote.search(match).group(1))
                jsonprinter['upstream']=parse_upstream(quote.search(match).group(1))
            elif qam.search(match):
                #print('Downstream: %s' % quote.search(match).group(1))
                jsonprinter['downstream']=parse_downstream(quote.search(match).group(1))
            elif bios.search(match):
                #print('BIOS: %s' % quote.search(match).group(1))
                jsonprinter['bios']=parse_bios(quote.search(match).group(1))
            else:
                print('Line match error')
print(json.dumps(jsonprinter, indent=4, sort_keys=True))
