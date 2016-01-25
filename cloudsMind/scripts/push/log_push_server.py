#!/usr/bin/env python
# -*- coding:UTF-8 -*-

#
# @filename:     log_push_server.py
# @description: 分析push_server的日志文件，得出总TPS
# @author:       zhaow
# @created:      2016-01-06
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

def downloadLog(t):
    c = push_key()
    ip = read_conf('PushServer', 'IP')
    username = read_conf('PushServer', 'UserName')
    port = read_conf('PushServer', 'Port')
    c.connect(ip, int(port), username, pkey=k)
    print "连接到PushServer ：%s" % (ip)
    stdin, stdout, stderr = c.exec_command('cat /var/log/cps-pushservice.log')
    lines = stdout.read()
    tempList = []
    for line in lines.splitlines():
        tempList.append(line)
    f = open('temp/cps-pushservice.log', 'w')
    for line in tempList:
        f.write(line + '\n')
    f.close()
    c.close()


# 写入数据
def write_excel(file,t):
    threads=read_conf('Threads','threadNums')
    threadnums=int(threads)
    linelist = []
    f = open('temp/cps-pushservice.log', 'r')
    lines = f.read()
    for line in lines.splitlines():
        if 'time' in line:
            linelist.append(line)
    nums=float(len(linelist))/threadnums
    #创建excel
    try:
        w = xlsxwriter.Workbook(file)
        ws=w.add_worksheet('push_server')
    except Exception, e:
        print str(e)
    avgList=[]
     #按照线程数进行循环
    for m in range(1,threadnums+1):
        ws.write(0,m-1,'Thread'+str(m)+'')
        i = 0
        timelist = []  # 存放消耗时间
        for n in range(1,int(math.floor(nums))+1):
            timelist.append(linelist[i+m-1])
            i += threadnums
        timel = []  # 存放日志输出的time=的时间
        for timeline in timelist:
            t = timeline.split(' ')[-1]
            timel.append(t.split('=')[-1])
        #写入time值
        num=1
        for time in timel:
            ws.write(num,m-1,time)
            num+=1
        ws.write(0,threadnums+m-1,'Thread'+str(m)+'的100个请求的响应时间'.decode('utf8'))
        #写入100个请求的响应时间
        i=0
        valuelist=[]
        for time in timel:
            if i<len(timel)-1:
                value=int(timel[i+1])-int(timel[i])
                valuelist.append(value)
                i+=1
                ws.write(i,threadnums+m-1,value)
        #计算每个线程的TPS
        ws.write(0,threadnums*2+m-1,'Thread'+str(m)+' TPS'.decode('utf8'))
        total=sum(valuelist)
        avg=float(1000*100)/(float(total)/len(valuelist))
        ws.write(1,threadnums*2+m-1,avg)
        avgList.append(avg)
    ws.write(0,threadnums*3,'总TPS'.decode('utf8'))
    ws.write(1,threadnums*3,sum(avgList))
    w.close()

def main():
    t=datetime.datetime.now().strftime('%m%d%H%M')
    logExcel='result/log_push_server'+t+'.xls'
    downloadLog(t)
    write_excel(logExcel,t)

if __name__ == '__main__':
    main()