#coding = utf-8
'''
   this is a SGFW API test script.
   getconfig() is used to get config from configfiles
   runconfig() is used to build the URI,and send http request to server
   logMessage() is used to log any messages
   if you want to test a function of SGFW,add it's config.txt to config/
   it's format is:
        arg1,arg2,arg3....
        value1,value2,value3....
'''
__author__ = 'ryan xue'
import httplib
import urllib
import time
import json
import sys
import paramiko,sqlite3

def getfile():
    t = paramiko.Transport("host",22)
    t.connect(username = "root", password = "password")
    sftp = paramiko.SFTPClient.from_transport(t)
    remotepath='/your/remote/file'
    localpath='/your/local/file/path'
    sftp.get(remotepath, localpath)
    t.close()

def getinfo(keyword,tablename,searchkey,searchvalue,dbs= "d:\\db.db3"):
    getfile()
    cx = sqlite3.connect(dbs)
    cu = cx.cursor()
    cu.execute("select %s from %s where %s =='%s'"%(keyword,tablename,searchkey,searchvalue))
    sqlresult = cu.fetchall()
    cx.commit()
    return str(sqlresult[0][0])

def getconfig(configname):
     p1 = {}
     f2 = open('config/'+configname,'r')
     for i in f2.readlines():
         aa = i.replace('\n','').split('=')
         p1[aa[0]]=aa[1]
     if configname == 'inetv4addr_eth1.txt':
         p1['uuid'] = getinfo('uuid','table','param','value')
     return p1
def runconfig(p1,apipath):
    conn = httplib.HTTPConnection("host","port")
    headers = {"Content-type": "application/x-www-form-urlencoded; charset=UTF-8", "Accept": "*/*"}
    params = urllib.urlencode({"username":"username", "password":"password"})
    conn.request("POST", "/login", params, headers)
    r = conn.getresponse()
    if r.status != 200 and r.status != 302:
        conn.close()
        print "login fault",r.status
        sys.exit(0)
    rrr = r.read()
    print urllib.urlencode(p1)
    cookie = json.loads(rrr)["Cookie"]
    headers = {"Content-type": "application/x-www-form-urlencoded; charset=UTF-8", "Accept": "*/*","Referer":"http://www.test.com/index"}
    headers["Cookie"]="tssession="+cookie
    conn.request("POST", apipath, urllib.urlencode(p1), headers)
    r2 = conn.getresponse()
    if r2.status == 200:
        res = r2.read()
        res = json.loads(res)
        if not res["success"]:
            ress = apipath +": rule not create, because:" + res["message"]
            logMessage(ress.encode('utf-8'))
        else:
            ress = apipath+": create success!"
            logMessage(ress.encode('utf-8'))
    else:
        ress = apipath + ": request fail",r2.read()
        logMessage(ress)

    conn.request("GET", "/system/config/apply")
    apply_req = conn.getresponse()
    if apply_req.status == 200:
        ress = apipath + ": rule apply success"
        logMessage(ress)
    else:
        ress = apipath + ": rule apply fail"
        logMessage(ress)

    conn.close()

def logMessage(message):
    fp = open('config/result.txt','a')
    fp.writelines(time.strftime("%Y-%m-%d %H:%M:%S") + message +'\n')
    fp.close()



if __name__ == '__main__':
    runconfig(getconfig('inetaddrv4_eth1.txt'),"/inet/addrv4Edit")
