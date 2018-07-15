#!/usr/bin/env python
import requests
from requests.auth import HTTPBasicAuth
import sys
from config import *
import re

client = requests.Session()
r = client.get(NETGEAR_URL)
r = client.get(NETGEAR_ROUTER_STATUS_URL, auth=(USERNAME,PASSWORD))
if r.status_code!=200:
    sys.exit("ERROR: Invalid status code %s" % r.status_code)

valuelist = re.compile(r'\<form\s+action=\x22\/goform\/RouterStatus\?id=(\d+)\x22\s+method=\x22post')
id = valuelist.search(r.text).group(1)

reboot_url = NETGEAR_RESET_URL + id
payload={'buttonSelect':'2','wantype':'dhcp','enable_apmode':'0'}
r = client.post(reboot_url, data=payload, auth=(USERNAME,PASSWORD))
if r.status_code!=200:
    sys.exit("ERROR: Invalid status code %s" % r.status_code)
