#!/usr/bin/env python
# -*- coding: utf-8 -*-
#"ids":["c558d5cd9c1e7f0128264f574627901620e0eb1d589acae604fd95454cf80051"]
import httplib
conn = httplib.HTTPConnection("192.168.0.245:8899")
# 2627c19c86a83be8bea3d22c2e3ff6ab64bd8c70e979e235423587c385b621f3
body = """{
    "appId":"com.cloudminds.ssdk.demo",
    "appKey":"securekey",
    "target":{
            "type":"APPTOKEN",
            "ids":["2627c19c86a83be8bea3d22c2e3ff6ab64bd8c70e979e235423587c385b621f3"]
    },
    "message":{
        "ios":"{\\"aps\\" : {\\"alert\\" : \\"Test push\\", \\"sound\\":\\"default\\"}}",
        "android":"{\\"aps\\" : {\\"alert\\" : \\"给您播放了一段铃声\\", \\"sound\\" : \\"sound.caf\\"},\\"cmd\\" : [\\"1\\"], \\"flownum\\":\\"51a148ae-207d-42a4-8b32-f73adb4d9cdd\\"}"
    },
    "signature":"ABCDEDFG00000=="
    }"""
print body

conn.request("POST","/cps-pushagent/cps/v1/push",body)

resp = conn.getresponse()
print resp.status, resp.reason

data = resp.read()

print "response:"
print(data)

conn.close()
