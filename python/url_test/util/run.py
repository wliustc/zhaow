# -*- coding:utf-8 -*-
import urllib2
from iniUtil import IniUtil
from cookieUtil import CookieUtil


cookieObj = CookieUtil()
iniObj = IniUtil('../config/url.ini')
cookie = cookieObj.getLoginCookie()
#获取配置文件的url
keysList = []
urlDict = {}
keysList = iniObj.getKeysBySection('url')
for key in keysList:
    pageCode = ''
    url = ''
    url = iniObj.getValue('url',key)
    urlDict.setdefault(key,url)
    #url = "http://kxyesit.cnsuning.com/"
    try:
        #创建请求的request
        req = urllib2.Request(url)
        handler = urllib2.HTTPCookieProcessor(cookie)
        #利用urllib2的build_opener方法创建一个opener
        openner = urllib2.build_opener(handler)
        responseCode = openner.open(req).getcode()
        #print '页面状态码为：' + str(responseCode)
        pageCode = u'状态码：' + str(responseCode)
        iniObj.setValue(section=u'状态码',key=key,value=pageCode)
    except urllib2.URLError,e:
        #print '错误原因：'+e.reason
        reason = e.reason
        pageCode = u'状态码：' + str(e.code) + u'  错误原因：' + reason
        #print pageCode
        iniObj.setValue(section=u'状态码',key=key,value=pageCode)
