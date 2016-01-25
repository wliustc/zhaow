#!/usr/bin/env python
# -*- coding:UTF-8 -*-

#
# @filename:     push_server.py
# @description: 开启pushserver服务
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


def pushServer_Start():
    c = push_key()
    ip = read_conf('PushServer', 'IP')
    username = read_conf('PushServer', 'UserName')
    port = read_conf('PushServer', 'Port')
    c.connect(ip, int(port), username, pkey=k)
    print '启动PushServer服务'
    c.exec_command('cd /opt/cps/cps-pushservice/;nohup /opt/cps/cps-pushservice/cps-pushservice /opt/cps/cps-pushservice/config.xml &')
    c.close()


def main():
    pushServer_Start()


if __name__ == '__main__':
    main()
