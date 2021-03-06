#!/usr/bin/env python3
import requests
import urllib.request
import json
import sys
import re
import argparse
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

parser = argparse.ArgumentParser()
parser.add_argument("-c","--config", nargs='+', help="config file")
args = parser.parse_args()

if args.config:
	if len(args.config)!=1:
		print('a config file is required')
		sys.exit(1)
else:
	print('a config file is required')
	sys.exit(1)

conf=args.config[0]
file = open(conf, 'r')
fsid = False

# read config files for keys and api endpoint
for line in file:
	if 'apikey' in line:
		apikey=(line.split("=")[1].rstrip('\n'))
	if 'secretkey' in line:
		secretkey=(line.split("=")[1].rstrip('\n'))
	if 'url' in line:
		url=str(line.split("=")[1].rstrip('\n'))

# create header
head = {}
head['api-key'] = apikey
head['secret-key'] = secretkey
head['content-type'] = 'application/json'

command = 'Storage/ActiveDirectory'
url = url+command

# get AD uuid
uuid = None
req = requests.get(url, headers = head)
data = (req.json())
for i in data:
	uuid=i['UUID']
if uuid is None:
	print("No Active Directory joined")
	sys.exit(1)

# delete AD
def delete_ad(uuid, url, head):
	url = url+'/'+uuid
	req = requests.delete(url, headers = head)
	details = json.dumps(req.json(), indent=4)
	print('Unjoining Active Directory')
	print(highlight(details, JsonLexer(), TerminalFormatter()))

delete_ad(uuid, url, head)