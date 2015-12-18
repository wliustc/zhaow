# -*- coding:UTF-8 -*-
import os
import urllib
import re
import urllib2
import shutil


def getRAR():
    url='http://www.22ba.com/article/Share481.html'
    # html=urllib.urlopen(url).read()
    f=urllib2.urlopen(url)
    urlList=[]
    for eachLine in f:
        if re.match('.*rar',eachLine):
            str=re.findall('http[:\\\\].*rar',eachLine)
            urlList.append(str)

    global downloadDir
    downloadDir='Download'
    if not os.path.exists(downloadDir):
        os.mkdir(downloadDir)
    else:
        shutil.rmtree(downloadDir)
        os.mkdir(downloadDir)
    dateList=[]
    for everyURL in urlList:
        wordItems = ''.join(everyURL).split('/')
        for item in wordItems:
            if re.match('.*\.rar$', item):
                rarName = item
                localPDF = os.path.join(downloadDir,rarName)
                # date=datetime.datetime.strptime(rarName[0:8],'%Y%m%d')
                dateList.append(rarName[0:8])
    sum=[]
    for date in dateList:
        sum.append(date)

    for everyURL in urlList:
        a=".*",sum[0],".*"
        b=r"".join(a)
        if re.match(b,''.join(everyURL)):
            str=everyURL
            try:
                urllib.urlretrieve(''.join(str),localPDF)
            except Exception,e:
                print '下载失败'
    return rarName

def unRAR(filename):
    # #windows RAR解压缩命令
    rar_command = 'UnRAR.exe x -y  -pwww.22ba.com  '+os.path.join(downloadDir,filename)+' '+downloadDir+''
    print rar_command
    if os.system(rar_command):
        print('successful!!!')



def shosts(downloadDir):
    for dirpath,dirnames,filenames in os.walk(downloadDir):
        for filename in filenames:
            if filename=='hosts':
                filepath=os.path.join(dirpath,filename)
                f=open(filepath,'r')
                lines=f.read()
                for index,line in enumerate(lines.splitlines()):
                    if re.match(r'^# Modify hosts start$', line):
                        iplist=lines.splitlines()[index:]
                f.close()
    return iplist

# C:\Windows\System32\drivers\etc\
#
def localhosts(hostslist):
    path='C:\Windows\System32\drivers\etc\hosts'
    temp=r'C:\Windows\System32\drivers\etc\temp'
    if os.path.exists(temp):
        os.remove(temp)
    f=open(path,'r')
    newfile=open(temp,'w')
    lines=f.read()
    lists=lines.splitlines()
    iplist=[]
    i=0
    for index,line in enumerate(lists):
        if re.match(r'^# Modify hosts start$',line):
            iplist=lists[index:]
            position=index
            while i<len(iplist):
                lists.remove(lists[position])
                i=i+1
    for l in lists:
        newfile.write(l+'\n')
    for m in hostslist:
        newfile.write(m+'\n')
    f.close()
    newfile.close()
    os.remove(path)
    os.rename(temp,path)
    shutil.rmtree(downloadDir)
    print '已经可以通过浏览器访问google了，去试一下！！！！！'

if __name__ == '__main__':
    filename=getRAR()
    unRAR(filename)
    iplist=shosts('Download')
    localhosts(iplist)



