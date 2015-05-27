#coding=utf-8
__author__ = 'Administrator'

import dns.resolver,time

def getdnsresult():
    domain = 'www.titansec.com.cn'
    goaldns=""
    ls =[]
    aa = dns.resolver.query(domain,'A')
    for i in aa.response.answer:
        for j in i.items:
            ls.append(j.address)
    if ls[0] != goaldns:
        mes=' oh my god! the dns record is wrong! eth expect result is %s,but the actual result is %s'%(goaldns,ls[0])
        logMessage(mes)
def logMessage(message):
    fp = open('dnsresult.txt','a')
    fp.writelines(time.strftime("%Y-%m-%d %H:%M:%S") + message +'\n')
    fp.close()

if __name__ == '__main__':
    while True:
        getdnsresult()
        time.sleep(1)