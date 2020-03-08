import re
import sys
import os, fnmatch
from pathlib import Path
from collections import Counter

args = sys.argv [1:]

parts = [
    r'(?P<host>\S+)',
    r'\S+',
    r'(?P<user>\S+)',               
    r'\[(?P<time>.+)\]',
    r'"(?P<request>.*)"',
    r'(?P<status>[0-9]+)',
    r'(?P<size>\S+)',
    r'"(?P<referrer>.*)"',
    r'"(?P<agent>.*)"',               
]

r = open(args[0])
log_data = []
pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')

def count():
    for line in r:
        try:
            log_data.append(pattern.match(line).groupdict())
        except:
            print("Coulnd't read all of the log lines")
    status_counter = Counter(x['status'] for x in log_data)
    print ("Log count of file: %s sorted by status:" % args[0])
    for x in status_counter.most_common(): 
        print ("\t%s Status %d times" % x)
        
def transferedBytes():
    sumo = 0
    for line in r:
        try:
            log_data.append(pattern.match(line).groupdict())
        except:
            print("Coulnd't read all of the log lines")
    sumOfTransferedBytes = Counter(x['size'] for x in log_data)
    print ("Bytes transeferd of file: %s" % args[0])
    for singleTransfer in sumOfTransferedBytes:
       try:
           sumo += int(singleTransfer)
       except:
           print("Cannot get all of the transfered bytes")
    print(sumo)

def file_len():
    with open(args[0]) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
        
def percentege():
    lineCount = 0
    for line in r:
        try:
            lineCount += 1
            log_data.append(pattern.match(line).groupdict())
        except:
            print("Coulnd't read all of the log lines")
    print ("Request percentege in file: %s" % args[0])
    print("Succesful requests: %.2f percent" % ((lineCount/file_len())*100))

if args:
    if os.path.exists(args[0]):
            if args[1].casefold() == "count":
                count()
            if args[1].casefold() == "percentege":
                percentege()
            if args[1].casefold() == "bytes":
                transferedBytes()
    else:
        print("File Path doesn't exist")
else:
    print("There is no files selected")

