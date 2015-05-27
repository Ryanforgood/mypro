#coding=utf-8
__author__ = 'ryan xue'


import paramiko
import sqlite3


def getfile():
    import paramiko
    host=""
    port=""
    password=""
    t = paramiko.Transport(host,port)
    t.connect(username = "root", password = password)
    sftp = paramiko.SFTPClient.from_transport(t)
    remotepath='/your/remote/file/path'
    localpath='/your/local/file/path'
    sftp.get(remotepath, localpath)
    t.close()

def getinfo(keyword,tablename,searchkey,searchvalue):
    cx = sqlite3.connect("d:\\db.db3")
    cu = cx.cursor()
    cu.execute("select %s from %s where %s =='%s'"%(keyword,tablename,searchkey,searchvalue))
    sqlresult = cu.fetchall()
    cx.commit()
    print str(sqlresult[0][0])
# if __name__ == '__main__':
    getfile()