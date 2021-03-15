#!/usr/bin/env python3
# 2021 Douglas Berdeaux
# Sorts out IP lists/ranges provided by clients
#   and creates a comma separated list of all expanded ranges/sets.
#
from netaddr import IPNetwork
import sys
from os import path
from re import match
from re import sub
import argparse
## Wow, this is a nice library! :)
parser = argparse.ArgumentParser(description='Process IP lists provided by client.')
parser.add_argument('--ipfile', dest='ip_file', metavar='(IP list file)',
                    help='File passed to iplistgen with IP ranges.')
args = parser.parse_args()

## Custom functions:
def error(msg):
    print(f"[!] ERROR: {msg}")
    sys.exit(1)

## OK, we got a file to test:
ip_file=args.ip_file
if path.isfile(ip_file): # File is OK:
    with open(ip_file,"r") as fh:
        for line in fh:
            range=line.rstrip()
            if(match("^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/[0-9]+$",range)):
                for ip in IPNetwork(range):
                    print(f"{ip},",end="")
            elif(match("^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+-[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$",range)):
                start_ip=range.split("-")[0]
                end_ip=range.split("-")[1]
                ip_123_oct = sub("\.[0-9]+$","",start_ip)
                start_oct=start_ip.split(".")[3]
                end_oct=end_ip.split(".")[3]
                if(int(start_oct)<int(end_oct)):
                    i = int(start_oct)
                    while i <= int(end_oct):
                        print(f"{ip_123_oct}.{i},",end="")
                        i+=1
                else:
                    error("IP Address range might be out of order.")
            elif(match("^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+-[0-9]+$",range)):
                start_ip=range.split("-")[0]
                ip_123_oct = sub("\.[0-9]+$","",start_ip)
                start_oct=range.split("-")[0].split(".")[3]
                end_oct=range.split("-")[1]
                if(int(start_oct)<int(end_oct)):
                    i = int(start_oct)
                    while i <= int(end_oct):
                        print(f"{ip_123_oct}.{i},",end="")
                        i+=1
                else:
                    error("IP Address range might be out of order.")
            elif(match("^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$",range)):
                print(f"{range},",end="")
else:
    error(f"Could not open file: {ip_file}")
print("") # clean up terminal
