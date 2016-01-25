#!/usr/bin/env python
# -*- coding:UTF-8 -*-

#
# @filename:     init.py
# @description:
#           pushSever()       #关闭pushserver队列及清空日志
#           clearRedis()      #清空redis中队列, 需要手动执行
#           pushPlatform()    #关闭push平台的服务
#           pushAgent()       #PushAgent服务重启
#           modifyThreads()   #修改PushServer的线程数
#           killClient()      #关闭所有客户端，及清空客户端接收日志
# @author:       zhaow
# @created:      2016-01-06
# @version:      0.1
#


import ConfigParser
import paramiko
import re
import redis
import time


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


# 1.PushServer队列关闭
# 2.清空PushServer日志
def pushSever():
    c = push_key()
    ip = read_conf('PushServer', 'IP')
    username = read_conf('PushServer', 'UserName')
    port = read_conf('PushServer', 'Port')
    c.connect(ip, int(port), username, pkey=k)
    print "连接到PushServer ：%s" % (ip)
    c.exec_command('pkill cps-pushservice')
    # stdin,stdout,stderr=c.exec_command('ps -ef|grep cps')
    # lines=stdout.read()
    # for line in lines.splitlines():
    #     if 'cps-pushservice' not in line:
    #         c.exec_command('pkill cps-pushservice')
    #         print 'CPS进程未kill成功！'
    #         pass

    print "PushServer 队列关闭完成"
    c.exec_command('&>/var/log/cps-pushservice.log')
    print 'PushServer 日志清空完成'
    c.close()


# 修改PushServer的开启的线程数
def modifyThreads():
    c = push_key()
    ip = read_conf('PushServer', 'IP')
    username = read_conf('PushServer', 'UserName')
    port = read_conf('PushServer', 'Port')
    threadnums = read_conf('Threads', 'threadNums')
    c.connect(ip, int(port), username, pkey=k)
    print "连接到PushServer ：%s" % (ip)
    stdin, stdout, stderr = c.exec_command('cat /opt/cps/cps-pushservice/config.xml')
    lines = stdout.read()
    tempList = []
    for line in lines.splitlines():
        tempList.append(line)
    n = '        <Worker count="' + threadnums + '" />'
    tempList[-3] = n
    f = open('temp/config.xml', 'w')
    for line in tempList:
        f.write(line + '\n')
    f.close()
    print 'PushServer 线程修改完成！'
    c.close()
    # 上传修改后的xml
    t = paramiko.Transport((ip, int(port)))
    t.connect(username=username, pkey=k)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put('temp/config.xml', '/opt/cps/cps-pushservice/config.xml')
    t.close()


# 关闭push平台的服务
def pushPlatform():
    c = push_key()
    ip = read_conf('PushPlatform', 'IP')
    username = read_conf('PushPlatform', 'UserName')
    port = read_conf('PushPlatform', 'Port')

    ipList = []
    for IP in ip.split(','):
        ipList.append(IP)
    print ipList
    for i in range(0, len(ipList)):
        print "连接到pushPlatform ：%s" % (ipList[i])
        c.connect(ipList[i], int(port), username, pkey=k)
        stdin, stdout, stderr = c.exec_command('/root/emqttd/bin/emqttd stop')
        out = stdout.read()
        if 'ok' in out:
            print '%s Push平台服务关闭成功！' %(ipList[i])
        elif 'Node is not running!' in out:
            print '%s Push平台服务已关闭！' %(ipList[i])
        else:
            print '%s Push平台服务关闭失败！' %(ipList[i])
        c.close()


# 1.PushAgent服务关闭
# 2.PushAgent服务开启
def pushAgent():
    c = push_key()
    ip = read_conf('PushAgent', 'IP')
    username = read_conf('PushAgent', 'UserName')
    port = read_conf('PushAgent', 'Port')
    print "连接到PushAgent ：%s" % (ip)
    c.connect(ip, int(port), username, pkey=k)
    c.exec_command('/root/tomcat8/bin/shutdown.sh')
    print 'PushAgent服务关闭！'
    time.sleep(5)
    c.exec_command('/root/tomcat8/bin/startup.sh')
    print 'PushAgent服务开启！'
    c.close()


# 清空redis数据
def clearRedis():
    ip = read_conf('Redis', 'IP')
    port = read_conf('Redis', 'Port')
    r = redis.Redis(host=ip, port=int(port), db=0)
    r.delete('CPS.QUEUE.ANDROID')
    length = r.llen('CPS.QUEUE.ANDROID')
    if length > 0:
        r.delete('CPS.QUEUE.ANDROID')
    elif length == 0:
        print 'Redis 清空完成！'


# 关闭所有客户端emqtt_bench_sub的进程
# 清空所有客户端接收日志
def killClient():
    c = push_key()
    ip = read_conf('Client', 'IPtotal')
    username = read_conf('Client', 'UserName')
    port = read_conf('Client', 'Port')
    for IP in ip.split(','):
        c.connect(IP, int(port), username, pkey=k)
        stdin, stdout, stderr = c.exec_command('ps -ef|grep emqtt')
        lines = stdout.read()
        for line in lines.splitlines():
            if re.match('.*emqtt_bench_sub.*', line):
                print ''.join(line.split(' ')[3:5])
                c.exec_command('kill -9 ' + ''.join(line.split(' ')[3:5]) + '')
        # c.exec_command('pkill emqttd')
        c.exec_command('rm -rf client*.log')
        c.close()
    print '客户端进程kill，日志清除'

def main():
    # pushSever()       #关闭pushserver队列及清空日志
    # clearRedis()      #清空redis中队列
    # time.sleep(10)
    killClient()      #关闭所有客户端，及清空客户端接收日志
    # pushPlatform()    #关闭push平台的服务
    # pushAgent()       #PushAgent服务重启
    # modifyThreads()   #修改PushServer的线程数



if __name__ == '__main__':
    main()
