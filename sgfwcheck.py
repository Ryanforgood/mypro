#coding=utf-8
__author__ = 'Administrator'
'''
    this  script is used to test sgfw.
    to check wether the created rule is the same with the backstage
'''
import httplib
import urllib
import time
import json
import string
import sys
import difflib
import paramiko,sqlite3


host = '192.168.36.164'
password = '050bdd95'

def logresult(message):
    fres = open('result.log','a')
    fres.write(time.strftime("%Y-%m-%d %H:%M:%S") + '\n')
    fres.write(message + '\n')
    fres.close()

def getconfigfile(remotefile,username='root'):
    '''
    todo: connect host by using sshlibrary
    :param host: the host you want to connect
    :param password: the password of root
    :param remotefile:the config file name include path
    :return:
    '''
    t = paramiko.Transport(host,22)
    t.connect(username = "root", password = password)
    sftp = paramiko.SFTPClient.from_transport(t)
    remotepath=remotefile
    localpath='d:\\dev\\'+str(remotefile.split('/')[-1])
    sftp.get(remotepath, localpath)
    t.close()

def readfile(filename):
    '''
    todo: read the file text
    :param filename:
    :return:
    '''
    try:
        filehandle=open(filename,'rb')
        text =filehandle.read().splitlines()
        filehandle.close()
        return text
    except IOError as error:
        print('Read file error:'+str(error))
        sys.exit()

def compare(local,remote):
    '''
    todo: compare the local config file and the config file getted by function getfile()
    :param local:
    :param remote:
    :return:
    '''
    local_file=readfile(local)
    remote_file=readfile(remote)
    d = difflib.HtmlDiff()
    fcom= open('result.html','w')
    fcom.write(d.make_file(local_file,remote_file))
    fcom.close()

def getprocessinfo(processname,result):
    '''
    todo: if the function has no config file,get it's info from system by shell code.such as 'ps -ef|grep tips'
    :param processname:
    :return:
    '''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host,22,"root", password)
    stdin, stdout, stderr = ssh.exec_command("ps -ef|grep %s" %processname)
    for i in stdout.readlines():
        if i.find(result)!= -1:
            message = 'the %s is on,and it\'s pid is %s' %(string.upper(processname),i[9:14])
            logresult(message)
    ssh.close()

def getdb():
    t = paramiko.Transport(host,22)
    t.connect(username = "root", password = password)
    sftp = paramiko.SFTPClient.from_transport(t)
    remotepath='/secone/sgfw/data/sgfw.db3'
    localpath='d:\\sgfw.db3'
    remotepath1='/secone/sgfw/data/localauth.db3'
    localpath1='d:\\localauth.db3'
    sftp.get(remotepath, localpath)
    sftp.get(remotepath1, localpath1)
    t.close()

def getdbinfo(keyword,tablename,searchkey,searchvalue,dbs= "d:\\sgfw.db3"):
    getdb()
    cx = sqlite3.connect(dbs)
    cu = cx.cursor()
    cu.execute("select %s from %s where %s =='%s'"%(keyword,tablename,searchkey,searchvalue))
    sqlresult = cu.fetchall()
    cx.commit()
    return str(sqlresult[0][0])


def getiptablesconfig(uuid,rulepre,mainchain):
    '''
    todo:get iptables rules
    :return:
    '''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host,22,"root", password)
    stdin, stdout, stderr = ssh.exec_command("iptables -vnL %s" %mainchain)
    for i in stdout.readlines():
        if i.find(uuid)!= -1:
            message = 'the %s rule is found,it is in %s,and it\'s rule is: \n%s' %(rulepre+uuid,mainchain,i)
            logresult(message)
            stdin, stdout, stderr = ssh.exec_command("iptables -vnL %s" %i[12:32])
            logresult(stdout.read())

    ssh.close()

if __name__ == '__main__':
    # getprocessinfo('192.168.36.164','050bdd95','tips','/secone/tips/bin/tips')
    # getconfigfile(host='192.168.36.165',password='8e87e3ca',remotefile='/etc/dhcp/dhcpd.conf')
    # compare('dhcpd.conf','dhcpd1.conf')
    getiptablesconfig(getdbinfo('uuid','sgfw_acl','alias','pptp-100内网'),'ACL_','SGFW_FWD_ACL')