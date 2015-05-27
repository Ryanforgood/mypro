#coding=utf-8
__author__ = 'ryan xue'


import paramiko
import sqlite3


def getfile():
    import paramiko
    t = paramiko.Transport("192.168.36.165",22)
    t.connect(username = "root", password = "8e87e3ca")
    sftp = paramiko.SFTPClient.from_transport(t)
    remotepath='/secone/sgfw/data/sgfw.db3'
    localpath='d:\\sgfw.db3'
    sftp.get(remotepath, localpath)
    t.close()

def getinfo(keyword,tablename,searchkey,searchvalue):
    cx = sqlite3.connect("d:\\sgfw.db3")
    cu = cx.cursor()
    cu.execute("select %s from %s where %s =='%s'"%(keyword,tablename,searchkey,searchvalue))
    sqlresult = cu.fetchall()
    cx.commit()
    print str(sqlresult[0][0])
# if __name__ == '__main__':
#     # getfile()
#     # getinfo('scope_parent','sgfw_obj_address','alias','99.99.99.0/24')