import httplib
import urllib
import time
import json
import sys


if __name__ == '__main__':
    conn = httplib.HTTPSConnection("192.168.36.165")
    
    params = urllib.urlencode({"username":"admin", "password":"admin"})
    headers = {"Content-type": "application/x-www-form-urlencoded; charset=UTF-8", "Accept": "*/*"}
    conn.request("POST", "/login", params, headers)
    r = conn.getresponse()
    if r.status != 200:
        conn.close()
        print "login fault"
        sys.exit(0)
    r.read()
    
    # dnat
    params = urllib.urlencode({"enable":"1", "alias":"1234", "src_type":"2", "src_ip":"", "src_object":"any",
                               "src_isp":"any", "src_reverse":"0", "dest":"eth1:192.168.1.1", "protocol":"TCP",
                               "protocol_port":"55", "action_type":"2", "convert_to":"2.2.2.2", "convert_port_type":"1",
                               "convert_port":"", "acl_enable":"0"})
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