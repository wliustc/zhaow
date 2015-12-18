#!/usr/bin/python
# -*- coding: UTF-8 -*-

#
# @filename:     SvnMigration.py
# @description:  Download source code from a svn repository and migration to anothor repository.
# @author:       Tian Meng
# @created:      2015-09-21 22:52:54
# @update:       2015-11-27  zhaow   新增文件对比，删除目标目录多余文件
# @version:      0.2
#

import time
import subprocess
import sys
import signal
import stat
import ConfigParser
import hashlib
import getopt
from filecmp import dircmp
import os
import shutil


def usage():
    print('''\

SvnMigration.py 

Download source code from a svn repository and migration to anothor repository.

A configuration file 'conf/svn.cnf' must be existed, options as follows:
[from]
url = http://10.27.164.97/svn/kxye/branches/kxye_V1.0.4
username = usera
password = 111111
 
[to]
url = http://10.27.164.97/svn/kxyezt/branches/kxyezt_V1.0.2
username = usera
password = 111111

EOF

Usage:
    python SvnMigration.py 
  
optional arguments:  
     -h, --help     show this help message and exit
     -v, --version  Version V1.0
''')


copyFileCounts = 0
oldSvn = None
newSvn = None


class Svn:
    """svn entity"""

    def __init__(self, url=None, username=None, password=None):
        self.__url = url
        self.__username = username
        self.__password = password

    def getUrl(self):
        return self.__url

    def getUserName(self):
        return self.__username

    def getPassWord(self):
        return self.__password


# 读取配置文件

def read_conf():
    try:
        cf = ConfigParser.ConfigParser()
        confDir = os.path.join(os.curdir, 'conf')
        confPath = os.path.join(confDir, 'svn.cnf')
        cf.read(confPath)

        global oldSvn
        global newSvn

        fromUrl = cf.get("from", "url")
        fromUsername = cf.get("from", "username")
        fromPassword = cf.get("from", "password")
        oldSvn = Svn(fromUrl, fromUsername, fromPassword)

        toUrl = cf.get("to", "url")
        toUsername = cf.get("to", "username")
        toPassword = cf.get("to", "password")
        newSvn = Svn(toUrl, toUsername, toPassword)

    except Exception, e:
        print('read conf/svn.cnf error')
        usage()
        sys.exit(-2)


def printProcess(p):
    """
    print subprocess stdout
    """
    r = p.stdout.read()
    lines = r.split("\n")
    for t in lines:
        print(t)


def on_rm_error(func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


def removeDir(targetDir):
    """
    recursion delete    
    """
    if os.path.isdir(targetDir):
        shutil.rmtree(targetDir, onerror=on_rm_error)
        print "dir " + targetDir + " removed"


def download(url, username, password, targetDir):
    """
    download from svn url
    """
    # osvn = 'svn export --force --username=1 --password=1 http://10.27.164.97/svn/sma/branches/SMA_V1.0.9'
    osvn = 'svn export --force '
    if username is not None:
        osvn = osvn + '--username=' + username + ' '
    if password is not None:
        osvn = osvn + '--password=' + password + ' '
    osvn = osvn + url + ' ' + targetDir
    # print(osvn)
    p = subprocess.Popen(osvn, shell=True, stdout=subprocess.PIPE)
    print('----------- start download... --------')
    printProcess(p)
    print('----------- download done! -----------')


def checkout(url, username, password, targetDir):
    """
    checkout from svn url
    """
    # osvn = 'svn co --force --username=1 --password=1 http://10.27.164.97/svn/sma/branches/SMA_V1.0.9'
    osvn = 'svn co --force '
    if username is not None:
        osvn = osvn + '--username=' + username + ' '
    if password is not None:
        osvn = osvn + '--password=' + password + ' '
    osvn = osvn + url + ' ' + targetDir
    p = subprocess.Popen(osvn, shell=True, stdout=subprocess.PIPE)
    print('----------- start checkout new repository... --------')
    printProcess(p)
    print('----------- checkout new repository done! -----------')


def addSvn(targetDir):
    # add
    print('----------- add file to svn --------')
    for parent, dirnames, filenames in os.walk(targetDir):
        # 3 params：1.parent folder 2.all folders（no path split '/'） 3. all
        # files name
        for dirname in dirnames:
            filepath = os.path.join(parent, dirname)
            if '.svn' in filepath:
                # print  ("dirname is" + filepath )
                pass
            else:
                addsvn = 'svn add ' + filepath + '/*'
                p = subprocess.Popen(
                    addsvn, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                r = p.stdout.read()
                lines = r.split("\n")
                for t in lines:
                    if (t.startswith('A')):
                        print(t)  # only print file has been added
    print('----------- add done! -----------')


def commit(username, password, targetDir):
    """
    commit to new svn
    """
    # osvn = 'svn commit -m "add test file for my test" '
    osvn = 'svn commit '
    if username is not None:
        osvn = osvn + '--username=' + username + ' '
    if password is not None:
        osvn = osvn + '--password=' + password + ' '
    osvn = osvn + '-m "commit by SvnMigration.py" ' + targetDir + '/*'
    # print(osvn)
    p = subprocess.Popen(osvn, shell=True, stdout=subprocess.PIPE)
    print('----------- start commit new repository... --------')
    printProcess(p)
    print('----------- commit done! -----------')


def getFileMd5(filename):
    """
    #get md5 by file
    """
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = file(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def copyFiles(sourceDir, targetDir):
    global copyFileCounts
    print sourceDir
    print u"%s dealing folder is :%s ,has processed %s files" % (
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), sourceDir, copyFileCounts)
    for f in os.listdir(sourceDir):
        sourceF = os.path.join(sourceDir, f)
        targetF = os.path.join(targetDir, f)
        if os.path.isfile(sourceF):
            # mkdir
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            copyFileCounts += 1

            # if file existed ,but file size is not equal
            if not os.path.exists(targetF) or (
                        os.path.exists(targetF) and (getFileMd5(targetF) != getFileMd5(sourceF))):
                # binary file
                open(targetF, "wb").write(open(sourceF, "rb").read())
                print u"%s %s copy done" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), targetF)
            else:
                pass
        if os.path.isdir(sourceF):
            copyFiles(sourceF, targetF)


def signal_handler(signal, frame):
    print('Exit!')
    sys.exit(0)


def help():
    #     parser = argparse.ArgumentParser(usage())
    #
    #     parser.add_argument("-v","--version",help="Version V1.0",action="store_true")
    #     # parser.add_argument("Download source code from a svn repository and migration to anothor repository.")
    #     args = parser.parse_args()
    #     if args.version:
    #         print "Version V1.0"
    #     else:
    #         print args.echo
    options, args = getopt.getopt(
        sys.argv[1:], "vh", ["version", "help"])
    for opt, value in options:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-v", "--version"):
            print("Version 1.0")
    sys.exit()


###比较文件夹，删除目标目录与原目录下不同的文件和目录
def deleteFile(rootDir, targetDir):
    dirobj = dircmp(rootDir, targetDir, ['.svn'])
    right_dir = dirobj.right_only
    for lists in right_dir:
        path = os.path.join(targetDir, lists)
        m = ''
        for i in path.split('/')[4:]:
            m = m + '/' + i
        if os.path.isdir(path):
            shutil.rmtree(path)
            deleteSvn(m)
        elif os.path.isfile(path):
            os.remove(path)
            deleteSvn(m)


###比较文件夹，相同的目录继续比较，不同目录删除
def compareDir(rootDir, targetDir):
    dirobj = dircmp(rootDir, targetDir, ['.svn'])
    common_dir = dirobj.common_dirs
    deleteFile(rootDir, targetDir)
    for lists in common_dir:
        path1 = os.path.join(rootDir, lists)
        path2 = os.path.join(targetDir, lists)
        deleteFile(path1, path2)
        compareDir(path1, path2)


def deleteSvn(targetDir):
    # delete
    # osvn='svn delete  'http://10.27.5.1/svn/byebuy/周报/smazt_V1.0.0/kxye-test/zhaow' -m 'delete zhaow''
    username = newSvn.getUserName()
    password = newSvn.getPassWord()
    osvn = 'svn delete '
    if username is not None:
        osvn = osvn + '--username=' + username + ' '
    if password is not None:
        osvn = osvn + '--password=' + password + ' '
    osvn = osvn + '-m "delete by SvnMigration.py" ' + ' ' + newSvn.getUrl() + targetDir + ' '
    p = subprocess.Popen(osvn, shell=True, stdout=subprocess.PIPE)
    print targetDir
    printProcess(p)


if __name__ == "__main__":
    help()
    signal.signal(signal.SIGINT, signal_handler)
    # read conf
    read_conf()
    workDir = os.path.join(os.curdir, 'work')
    oldFolder = os.path.join(workDir, 'from', oldSvn.getUrl().split('/')[-1])
    newFolder = os.path.join(workDir, 'to', newSvn.getUrl().split('/')[-1])

    # export old svn
    print('\nold svn will export to this folder: ' + oldFolder)
    removeDir(oldFolder)
    download(oldSvn.getUrl(), oldSvn.getUserName(),
             oldSvn.getPassWord(), oldFolder)

    # checkout new svn
    print('\nnew svn will checkout to this folder: ' + newFolder)
    removeDir(newFolder)
    checkout(newSvn.getUrl(), newSvn.getUserName(),
             newSvn.getPassWord(), newFolder)

    # 新旧文件夹对比，删除新文件中不同的文件和目录
    print('----------- from svn delete file --------')
    compareDir(oldFolder, newFolder)
    print('----------- delete done! -----------')

    """
        svn 命令提交，如果目录下有删除提交不成功，所以采用
    """
    print('\nnew svn will checkout to this folder: ' + newFolder)
    removeDir(newFolder)
    checkout(newSvn.getUrl(), newSvn.getUserName(),
             newSvn.getPassWord(), newFolder)


    print('----------- copy to new svn repository ! -----------')
    copyFiles(oldFolder, newFolder)
    print('----------- copy done ! -----------')

    # add to svn
    addSvn(newFolder)

    # commit
    print(
        '\n' + newFolder + ' will be commited in 15s, press CTRL + C to stop it')
    count = 0
    while (count < 15):
        ncount = 15 - count
        print ncount
        time.sleep(1)
        count += 1
    commit(newSvn.getUserName(), newSvn.getPassWord(), newFolder)
