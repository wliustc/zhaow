# -*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib
import re

class CookieUtil:

    def __init__(self):
        self.fileName = '../config/cookie.txt'
        self.loginUrl = 'https://passport.suning.com/ids/login?method=GET&loginTheme=b2c'
        self.vCodeName = "../config/vcode.png"
        #MozillaCookieJar提供可读写操作的cookie文件,存储cookie对象
        self.cookiejar = cookielib.MozillaCookieJar(self.fileName)

    #获取登录页面的response信息，用来获取cookie和uuid
    def getLoginPageResp(self):
        #将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
        cookieSupport= urllib2.HTTPCookieProcessor(self.cookiejar)
        #创建一个opener，将保存了cookie的http处理器，还有设置一个handler用于处理http的
        opener = urllib2.build_opener(cookieSupport)
        #将包含了cookie、http处理器、http的handler的资源和urllib2对象绑定在一起，安装opener,此后调用urlopen()时都会使用安装过的opener对象，
        urllib2.install_opener(opener)
        #获取uuid
        sn = urllib2.urlopen(self.loginUrl)
        resp = sn.read()
        return resp
        #保存cookie到文件
        #cookiejar.save(ignore_discard=True,ignore_expires=True)

    #获取uuid
    def getUuid(self,loginPageResp):
        #打开验证码
        pattern = re.compile('var uuid = "(.*?)";',re.S)
        matchResult = re.search(pattern,loginPageResp)
        uuid = matchResult.group(1)
        #print "uuid::"+uuid
        return uuid

    #储存图片
    def saveVCodeImg(self,uuid):
        imgurl = "https://vcs.suning.com/vcs/imageCode.htm?uuid="+uuid+"&yys="
        request = urllib2.Request(imgurl)
        response = urllib2.urlopen(request)
        content = response.read()
        fp = open(self.vCodeName,"wb")
        fp.write(content)
        fp.close()

    #存储登录后cookie
    def saveLoginCookie(self,userName,passWord,uuid,vcode):
        data = urllib.urlencode({
            'username':userName,
            'password':passWord,
            'jsonViewType':'true',
            'loginTheme':'b2c',
            "uuid":uuid,
            'verifyCode':vcode
        })
        request = urllib2.Request(self.loginUrl,data=data)
        response = urllib2.urlopen(request)
        #保存cookie到文件
        self.cookiejar.save(ignore_discard=True,ignore_expires=True)

    #获取cookie
    def getCookie(self):
        #创建MozillaCookieJar实例对象
        cookieFromFile = cookielib.MozillaCookieJar()
        #从文件中读取cookie内容到变量
        cookieFromFile.load(self.fileName,ignore_expires=True,ignore_discard=True)
        return cookieFromFile

    #直接获取登录后cookie
    def getLoginCookie(self):
        resp_ = self.getLoginPageResp()
        uuid_ = self.getUuid(resp_)
        self.saveVCodeImg(uuid_)
        #输入验证码
        vcode_ = raw_input("输入验证码 :")
        username_ = '251055836@qq.com'
        password_ = 'yxz0521'
        self.saveLoginCookie(userName=username_,passWord=password_,uuid=uuid_,vcode=vcode_)
        returnCookie = self.getCookie()
        return returnCookie