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
    t = paramiko.Transport("192.168.36.165",22)
    t.connect(username = "root", password = "8e87e3ca")
    sftp = paramiko.SFTPClient.from_transport(t)
    remotepath='/secone/sgfw/data/sgfw.db3'
    localpath='d:\\sgfw.db3'
    remotepath1='/secone/sgfw/data/localauth.db3'
    localpath1='d:\\localauth.db3'
    sftp.get(remotepath, localpath)
    sftp.get(remotepath1, localpath1)
    t.close()

def getinfo(keyword,tablename,searchkey,searchvalue,dbs= "d:\\sgfw.db3"):
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
         p1['uuid'] = getinfo('uuid','sgfw_inet_ipv4','dev','eth1')
     if configname == 'dhcpvlan22.txt':
         p1['pool_member'] = getinfo('uuid','sgfw_dhcp_pool','alias','vlan22')
     if configname == 'dhcpvlan33.txt':
         p1['pool_member'] = getinfo('uuid','sgfw_dhcp_pool','alias','vlan33')
     if configname == 'connlimit.txt':
         p1['source'] = getinfo('scope_parent','sgfw_obj_address','alias','99.99.99.0/24')
     if configname == 'ipsecmobile.txt':
         p1['p1']=getinfo('uuid','sgfw_ipsec_p1','alias','des-3des-md5-sha1-dh_group2')
         p1['p2']=getinfo('uuid','sgfw_ipsec_p2','alias','des_3des-md5_sha1-PFS2')
     if configname == 'snat.txt':
         p1['source'] = getinfo('scope_parent','sgfw_obj_address','alias','99.99.99.0/24')
     if configname == 'ssltunnelrule.txt':
         bb= getinfo('group_info','sgfw_vpn_user','username','test','d:\\localauth.db3')
         p1['usergroup']=bb[2:-2]
     if configname == 'sslwebrule.txt':
         bb= getinfo('group_info','sgfw_vpn_user','username','test','d:\\localauth.db3')
         p1['usergroup']=bb[2:-2]
         p1['resource']=getinfo('uuid','sgfw_sslvpn_resource','alias','web')
     return p1
def runconfig(p1,apipath):
    conn = httplib.HTTPConnection("192.168.36.165","8080")
    headers = {"Content-type": "application/x-www-form-urlencoded; charset=UTF-8", "Accept": "*/*"}
    params = urllib.urlencode({"username":"admin", "password":"admin"})
    conn.request("POST", "/login", params, headers)
    r = conn.getresponse()
    if r.status != 200 and r.status != 302:
        conn.close()
        print "login fault",r.status
        sys.exit(0)
    rrr = r.read()
    print urllib.urlencode(p1)
    cookie = json.loads(rrr)["Cookie"]
    headers = {"Content-type": "application/x-www-form-urlencoded; charset=UTF-8", "Accept": "*/*","Referer":"http://192.168.36.165:8080/index"}
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
    # runconfig(getconfig('dnat.txt'),"/dnat/create")
    runconfig(getconfig('snat.txt'),"/snat/create")
    # runconfig(getconfig('addr_net.txt'),"/addr/create")
    # runconfig(getconfig('addr_address.txt'),"/addr/create")
    # runconfig(getconfig('inetaddrv4_eth1.txt'),"/inet/addrv4Edit")
    # runconfig(getconfig('vlan1.txt'),"/inet/createVlan")
    # runconfig(getconfig('vlan2.txt'),"/inet/createVlan")
    # runconfig(getconfig('vlan1addr.txt'),"/inet/addrv4Create")
    # runconfig(getconfig('vlan2addr.txt'),"/inet/addrv4Create")
    # runconfig(getconfig('dhcppool1.txt'),"/dhcp/createPool")
    # runconfig(getconfig('dhcppool2.txt'),"/dhcp/createPool")
    # runconfig(getconfig('dhcpvlan22.txt'),"/dhcp/create")
    # runconfig(getconfig('dhcpvlan33.txt'),"/dhcp/create")
    # runconfig(getconfig('macbonding.txt'),"/macbind/create")
    # runconfig(getconfig('arpprotect.txt'),"/sysconfig/setArpConfig")
    # runconfig(getconfig('ips.txt'),"/ips/create")
    # runconfig(getconfig('dos.txt'),"/dos/create")
    # runconfig(getconfig('connlimit.txt'),"/climit/create")
    # runconfig(getconfig('appcc.txt'),"/appcc/create")
    # runconfig(getconfig('serverprotect.txt'),"/appcc/createStrategy")
    # runconfig(getconfig('radius.txt'),"/radiusClient/create")
    # runconfig(getconfig('vpnuser.txt'),"/sslvpn/createSslvpnUser")
    # runconfig(getconfig('ssltunnel.txt'),"/sslvpn/tunnelCreate")
    # runconfig(getconfig('sslweb.txt'),"/sslvpn/resource/create")
    runconfig(getconfig('ssltunnelrule.txt'),"/sslvpn/role/create")
    runconfig(getconfig('sslwebrule.txt'),"/sslvpn/role/create")
    # runconfig(getconfig('ipsecmobile.txt'),"/vpnipsec/setMobielConnConfig")
    # runconfig(getconfig('pptp.txt'),"/pptp/save")
