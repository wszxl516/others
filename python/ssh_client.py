#!/usr/local/bin/python3
import paramiko as pa
sshclient = pa.SSHClient()
sshclient.set_missing_host_key_policy(pa.AutoAddPolicy())
sshclient.connect('162.166.3.199',22,'zxl','*****')
stdin, stdout, stderr= sshclient.exec_command('ls -a')
print(stdout.readlines())
