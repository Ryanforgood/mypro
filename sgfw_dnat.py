import httplib
import urllib
import time
import json
import sys


if __name__ == '__main__':
    host = ""
    conn = httplib.HTTPSConnection(host)
    
    params = urllib.urlencode({"username":"usernanme", "password":"password"})
    headers = {"Content-type": "application/x-www-form-urlencoded; charset=UTF-8", "Accept": "*/*"}
    conn.request("POST", "/login", params, headers)
    r = conn.getresponse()
    if r.status != 200:
        conn.close()
        print "login fault"
        sys.exit(0)
    r.read()
    
    # dnat
    params =urllib.urlencode({"param1":"value1","param2":"value2"})
    headers = {"Content-type": "application/x-www-form-urlencoded; charset=UTF-8", "Accept": "*/*"}
    conn.request("POST", "/dnat/create", params, headers)
    r2 = conn.getresponse()
    if r2.status == 200:
        res = r2.read()
        res = json.loads(res)
        if not res["success"]:
            print "rule not create, because:" + res["message"]
    else:
        print "request fail"
    
    
    conn.request("GET", "/system/config/apply")
    apply_req = conn.getresponse()
    if apply_req.status == 200:
        print "apply success"
    else:
        print "apply fail"

    conn.close()