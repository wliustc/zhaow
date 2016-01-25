#!/usr/bin/env python
# -*- coding:UTF-8 -*-

#
# @filename:     push_platform.py
# @description: 开启push_platform服务
# @author:       zhaow
# @created:      2016-01-06
# @version:      0.1
#
import ConfigParser
import paramiko


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


def pushPlatform_Start():
    c = push_key()
    ip = read_conf('PushPlatform', 'IP')
    username = read_conf('PushPlatform', 'UserName')
    port = read_conf('PushPlatform', 'Port')

    ipList = []
    for IP in ip.split(','):
        ipList.append(IP)
    print ipList
    for i in range(0, len(ipList)):
        c.connect(ipList[i], int(port), username, pkey=k)
        stdin, stdout, stderr = c.exec_command('/root/emqttd/bin/emqttd start')
        out = stdout.read()
        if 'successfully' in out:
            print '%s Push平台服务启动成功！' %(ipList[i])
        elif 'Node is already running!' in out:
            print '%s Push平台服务已经启动！'%(ipList[i])
        else:
            print '%s Push平台服务启动失败！'%(ipList[i])
        c.close()


def main():
    pushPlatform_Start()


if __name__ == '__main__':
    main()
