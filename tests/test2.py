#-*- coding:UTF-8 -*-
import cookielib
import urllib2

#设置保存cookie的文件，同级目录下的cookie.txt
filename = 'cookie11.txt'
#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)
#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
handler = urllib2.HTTPCookieProcessor(cookie)
#通过handler来构建opener
opener = urllib2.build_opener(handler)
#创建一个请求，原理同urllib2的urlopen
response = opener.open("https://passport.suning.com/ids/login?service=https%3A%2F%2Faq.suning.com%2Fasc%2Fauth%3FtargetUrl%3Dhttp%253A%252F%252Fshopping.suning.com%252Fab.do%253Fcallback%253DjQuery172008723152778111398_1452738143630%2526_%253D1452738144124&gateway=true&loginTheme=b2c")
#保存cookie到文件
cookie.save(ignore_discard=True, ignore_expires=True)