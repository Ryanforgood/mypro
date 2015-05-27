# -*- coding: utf-8 -*-
__author__ = 'Administrator'

import xlsxwriter
import sys
import smtplib
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


reload(sys)
sys.setdefaultencoding('utf8')

def testworkmail():
    HOST = 'smtp.titansec.com.cn'
    TO = ['xuelj@titansec.com.cn','wangyan@titansec.com.cn','guyy@titansec.com.cn','caoxd@titansec.com.cn']
    FROM = 'xuelj@titansec.com.cn'
    SUBJECT = '本周工作'
    text = "各位好，本周的工作如附件所示，请大家自行领取，注意更新进度"
    # BODY = string.join((
    #     "From: %s" % FROM,
    #     "To: %s" % TO,
    #     "Subject: %s" % SUBJECT,
    #     "",
    #     text
    # ),"\r\n")
    msg = MIMEMultipart('related')
    attach = MIMEText(open("Weekly_work.xlsx",'rb').read(),"base64","utf-8")
    attach["Content-Type"] = "application/octet-stream"
    attach["Content-Disposition"]="attachment;filename=\"本周工作.xlsx\""
    msg.attach(attach)
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    toAll = []
    if TO[0]:
        msg['To'] = COMMASPACE.join(TO)
        [toAll.append(i) for i in TO]
    server = smtplib.SMTP()
    server.connect(HOST,"25")
    server.login("xuelj@titansec.com.cn","titan1")
    server.sendmail(FROM,TO,msg.as_string())
    server.quit()

def getconfig():
    bb=[]
    cc=[]
    dd=[]
    filepath = raw_input("Input your file name: ")
    prodpath = raw_input("Input your product name: ")
    f = open(filepath,'r')
    f = f.read().replace('---------------------\n','')
    d = open(prodpath,'w')
    d.write(f)
    d.close()

    fp=open(prodpath,'r')
    for i in  fp.readlines():
        aa = i.replace('\n','')
        bb.append(aa)
    for i in range(0,len(bb),1):
        if i%2==0:
            cc.append(bb[i])
        else:
            dd.append(bb[i])
    fp.close()

    workbook = xlsxwriter.Workbook('Weekly_work.xlsx')
    if prodpath == 'SGFW' or prodpath == 'sgfw' :
        worksheet = workbook.add_worksheet(prodpath)
        worksheet.write(0,0,'提交号')
        worksheet.write(0,1,'提交内容')
        worksheet.write(0,2,'产品')
        worksheet.write(0,3,'分支')
        worksheet.write(0,4,'执行结果')
        for i in range(1,len(cc),1):
            worksheet.write(i,0,cc[i])
            worksheet.write_string(i,1,dd[i])
            worksheet.write(i,2,'SGFW')
            worksheet.write(i,3,'V3')
    if prodpath == 'WAF'or prodpath == 'waf':
        worksheet = workbook.add_worksheet(prodpath)
        worksheet.write(0,0,'提交号')
        worksheet.write(0,1,'提交内容')
        worksheet.write(0,2,'产品')
        worksheet.write(0,3,'分支')
        worksheet.write(0,4,'执行结果')
        for i in range(1,len(cc),1):
            worksheet.write(i,0,cc[i])
            worksheet.write_string(i,1,dd[i])
            worksheet.write(i,2,'WAF')
            worksheet.write(i,3,'TRUNK')
    workbook.close()

if __name__ == '__main__':
    getconfig()
    testworkmail()