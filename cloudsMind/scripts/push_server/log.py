#!/usr/bin/python
# -*- coding:utf-8 -*-


import math
import xlsxwriter

#
# @filename:     log.py
# @description:  用于分析队列到pushserver的日志
# @author:       zhaow
# @created:      2016-01-04
# @version:      0.1
#


# 写入数据
def write_excel(file,threadnums):
    linelist = []
    f = open('cps-pushservice.log', 'r')
    lines = f.read()
    for line in lines.splitlines():
        if 'time' in line:
            linelist.append(line)
    nums=float(len(linelist))/threadnums
    #创建excel
    try:
        w = xlsxwriter.Workbook(file)
        ws=w.add_worksheet('log')
    except Exception, e:
        print str(e)

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
        # ws.set_column(threadnums+m-1,160)
        #写入100个请求的响应时间
        i=0
        valuelist=[]
        for time in timel:
            if i<len(timel)-1:
                value=int(timel[i+1])-int(timel[i])
                valuelist.append(value)
                i+=1
                ws.write(i,threadnums+m-1,value)
        ws.write(0,threadnums*2+m-1,'Thread'+str(m)+' TPS'.decode('utf8'))
        total=sum(valuelist)
        avg=float(1000*100)/(float(total)/len(valuelist))
        ws.write(1,threadnums*2+m-1,avg)
    w.close()



if __name__ == '__main__':
    excel_file = 'log.xls'
    threadnums=2
    write_excel(excel_file,threadnums)
