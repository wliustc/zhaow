#!/usr/bin/env python
# -*- coding: utf-8 -*-
#"ids":["c558d5cd9c1e7f0128264f574627901620e0eb1d589acae604fd95454cf80051"]
import httplib
import urllib2

# proxy = urllib2.ProxyHandler({'http': '127.0.0.1:8888'})
# opener = urllib2.build_opener(proxy)
# urllib2.install_opener(opener)
httplib.HTTPConnection.debuglevel = 1
conn = httplib.HTTPConnection("192.168.0.241:8899")
# 2627c19c86a83be8bea3d22c2e3ff6ab64bd8c70e979e235423587c385b621f3
body = """{
    "appId":"com.cloudminds.ssdk.demo",
    "appKey":"securekey",
    "target":{
            "type":"APPTOKEN",
            "ids":["1234567890"]
    },
    "message":{
        "ios":"{\\"aps\\" : {\\"alert\\" : \\"Test push\\", \\"sound\\":\\"default\\"}}",
        "android":"{\\"aps\\" : {\\"alert\\" : \\"给您播放了一段铃声\\", \\"sound\\" : \\"sound.caf\\"},\\"cmd\\" : [\\"1\\"], \\"flownum\\":\\"51a148ae-207d-42a4-8b32-f73adb4d9cdd\\"}"
    },
    "signature":"ABCDEDFG00000=="
    }"""

conn.request("POST","/cps-pushagent/cps/v1/push",body)

resp = conn.getresponse()
print resp.status, resp.reason,resp.getheaders()

data = resp.read()

print "response:"
print(data)

conn.close()