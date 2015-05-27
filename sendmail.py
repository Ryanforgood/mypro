#coding=utf-8
__author__ = 'Administrator'

import smtplib
import string

HOST = 'smtp.titansec.com.cn'
SUBJECT = 'the worklist of This week for SGFW'
TO = 'xuelj@titansec.com.cn'
FROM = 'xuelj@titansec.com.cn'
text = 'test'

BODY = string.join((
    "From: %s" % FROM,
    "To: %s" % TO,
    "Subject: %s" % SUBJECT,
    "",
    text
    ),"\r\n")
server = smtplib.SMTP()
server.connect(HOST,"25")
# server.starttls()
server.login("xuelj@titansec.com.cn","titan1")
server.sendmail(FROM,[TO],BODY)
server.quit()
