#!/usr/bin/env python
# -*- coding:UTF-8 -*-

#
# @filename:     log_push_client.py
# @description: 分析client的日志文件，得出总TPS
# @author:       zhaow
# @created:      2016-01-07
# @version:      0.1
#
import ConfigParser

import datetime
import paramiko
import math
import xlsxwriter

def read_conf(section, key):
    config = ConfigParser.ConfigParser()
    config.read('conf/conf.ini')
    return config.get(section, key)


def push_key():
    global k
    k = paramiko.RSAKey.from_private_key_file('conf/emm-push-key.pem')
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    return c

def downloadLog(logExcel,t):
    c = push_key()
    ip = read_conf('Client', 'IPtotal')
    username = read_conf('Client', 'UserName')
    port = read_conf('Client', 'Port')
    ipList = []
    for IP in ip.split(','):
        ipList.append(IP)
    #创建excel
    try:
        w = xlsxwriter.Workbook(logExcel)
        ws=w.add_worksheet('client_log')
        ws1=w.add_worksheet('TPS')
        ws.set_column('A:Z',50)
        ws1.set_column('A:Z',20)
    except Exception, e:
        print str(e)
    print ipList
    for i in range(0, len(ipList)):
        c.connect(ipList[i], int(port), username, pkey=k)
        stdin,stdout,stderr=c.exec_command('cat /home/ubuntu/client'+ipList[i]+'.log')
        lines = stdout.read()
        tempList = []
        for line in lines.splitlines():
            tempList.append(line)
        f = open('temp/client'+ipList[i]+'.log', 'w')
        for line in tempList:
            f.write(line + '\n')
        f.close()
        c.close()
        write_excel(logExcel,ipList[i],ws,i,ws1)
    # ws1.write(1,2,'=SUM(A2:B2)')
    w.close()

# 写入数据
def write_excel(file,ip,ws,i,ws1):
    linelist = []
    f = open('temp/client'+ip+'.log', 'r')
    lines = f.read()
    row=0
    ws.write(0,i,ip)
    ws1.write(0,i,ip)

    rowList=[]
    for line in lines.splitlines():
        if 'recv' in line:
            linelist.append(line)
            row+=1
            ws.write(row,i,line)
            str=line.split(',')[-1].split('=')[-1].split('(')[0]
            ws1.write(row,i,int(str))
            rowList.append(int(str))
    if row>0:
        avg=float(sum(rowList))/row
        ws1.write(row+2,i,avg)



def main():
    t=datetime.datetime.now().strftime('%m%d%H%M')
    logExcel='result/log_push_client'+t+'.xls'
    downloadLog(logExcel,t)
    # write_excel(logExcel,t)

if __name__ == '__main__':
    main()