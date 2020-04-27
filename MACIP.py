import os
import json
import logging as logger
from logging import getLogger, StreamHandler, DEBUG
from datetime import datetime, timedelta, tzinfo
from commands import getoutput
import jaconv
import random, string

mac_list = []
ip_fmt = "10.0.1.%s"

def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

class JST(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=9)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return 'JST'

def applytimezonejst():
    _dt = datetime.now(tz=JST())
    _dt2 = _dt.replace(tzinfo=JST())\
            .astimezone(JST())\
            .strftime("%Y/%m/%d %H:%M:%S %Z %z")
    return _dt2

for i in range(255):
    ip = ip_fmt % i
    line = getoutput('arp %s' % ip)
    macaddr = line.split(' ')[3]
    if "-- no entry" not in line:
        macaddr = line.split(' ')[3]
        mac_list.append((ip, macaddr))

data = {}
with open('oui.txt') as f:
    i = 0
    for s_line in f:
        i = i + 1
        if i < 5:
            continue
        p = i % 6
        if p == 0:
            mac = s_line.split("     (base 16)\t\t")[0].strip("\n")
            inc = s_line.split("     (base 16)\t\t")[1].strip("\n")
            data[mac] = [inc]
            if inc == "Private":
                i = i + 3
        if p == 3:
            ccltd = s_line.strip()
            data[mac].append(ccltd)

tmp_list = []
for x in mac_list:
    item = x[1].split(":")
    try:
        main = item[0] + item[1] + item[2]
        main = main.upper()
        tmp_list.append(main)
    except:
        pass

tmp_main = []
tmp_sys = []

def sysLogOpen():
    syslog_open = open('syslog_test.json', 'r')
    syslog_open = json.load(syslog_open)
    return syslog_open

for x in tmp_list:
    try:
        d = {
            "name": data[x],
        }
        tmp_main.append(d)
    except:
        pass
    try:
        user_name = randomname(5)
        dic = {
            "name": data[x],
            "user": user_name,
            "date": applytimezonejst()
        }
        tmp_sys.append(sysLogOpen())
        tmp_sys.append(dic)
    except:
        pass

    with open('syslog_test.json', 'w') as f:
        json.dump(tmp_sys, f, indent=2, ensure_ascii=False)

    formatter = '%(levelname)s : %(thread)d : %(process)d : %(name)s : %(asctime)s : %(lineno)d : %(message)s'
    logger.basicConfig(filename="syslog_test.log" , level=DEBUG, format=formatter)
    try:
        logger.info('%s', d)
    except:
        pass
