# -*- coding:UTF-8 -*-
import os
import shutil
import urllib
import urllib2

import re

from selenium import webdriver

url = 'https://passport.suning.com/ids/login'
urlList = []
f = urllib2.urlopen(url)
# html=urllib.urlopen(url).read()
# print html

driver = webdriver.PhantomJS()
driver.get(url)
#获取验证码src
vcodeimgElement = driver.find_element_by_id("vcodeimg1")
vcodeimg = vcodeimgElement.get_attribute("src")
print vcodeimg

for eachline in f:
    if re.match('.*https://vcs.suning.com/vcs/imageCode.htm.*', eachline):
        str = re.findall('https://vcs.suning.com/vcs/imageCode.*=', eachline)
        urlList.append(str)
downloadDir = 'Download'
if not os.path.exists(downloadDir):
    os.mkdir(downloadDir)
else:
    shutil.rmtree(downloadDir)
    os.mkdir(downloadDir)
localPDF = os.path.join(downloadDir, '123.png')
for everyURL in urlList:
        str = everyURL
        try:
            urllib.urlretrieve(''.join(str), localPDF)
        except Exception, e:
            print '下载失败'

print urlList
