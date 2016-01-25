#!/usr/bin/python
# -*- coding:utf-8 -*-
import threading
import subprocess
import os
import sys

import datetime

sshport = 13131
log_path = 'update_log'
output = {}
def execute(s, ip, cmd, log_path_today):
    with s:
        cmd = '''ssh -p%s root@%s -n "%s" ''' % (sshport, ip, cmd)
        ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output[ip] = ret.stdout.readlines()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: %s config.ini cmd" % sys.argv[0]
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print "Usage: %s is not file!" % sys.argv[1]
        sys.exit(1)

    cmd = sys.argv[2]

    f = open(sys.argv[1],'r')
    list = f.readlines()
    f.close()
    today = datetime.date.today()
    log_path_today = '%s/%s' % (log_path,today)
    if not os.path.isdir(log_path_today):
        os.makedirs(log_path_today)

    threading_num = 100
    if threading_num > len(list):
        threading_num = len(list)
    s = threading.Semaphore(threading_num)

    for line in list:
        ip = line.strip()
        t = threading.Thread(target=execute,args=(s, ip,cmd,log_path_today))
        t.setDaemon(True)
        t.start()

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()

    for ip,result in output.items():
        print "%s: " % ip
        for line in result:
            print "    %s" % line.strip()

    print "Done!"