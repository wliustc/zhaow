#!/usr/bin/env python
import paramiko
ip='54.223.83.133'
username='root'
port=22
# paramiko.util.log_to_file('ssh.log')
def fun():
    k = paramiko.RSAKey.from_private_key_file('emm-push-key.pem')
    # c = paramiko.SSHClient()
    # c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # print "Starting"
    # c.connect(ip,port,username,pkey=k)
    # return c
    t=paramiko.Transport((ip,port))
    t.connect(username=username,pkey=k)
    # t.connect(username=username,password='Cloud1688')
    print t   #<paramiko.Transport at 0x2d64f60L (cipher aes128-ctr, 128 bits) (active; 0 open channel(s))>
    sftp=paramiko.SFTPClient.from_transport(t)
    sftp.put('config.xml','/opt/config.xml')
    t.close()

if __name__ == '__main__':
    fun()