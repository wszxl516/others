#!/usr/local/bin/python3
import paramiko as pa
sshclient = pa.SSHClient()
sshclient.set_missing_host_key_policy(pa.AutoAddPolicy())
sshclient.connect('162.166.3.200',22,'zxl','wszxl516')
shell = sshclient.invoke_shell()
shell.send(b'su - root\n')
while 1:
    stdout = shell.recv(10240)
    res = stdout.decode()
    print(res)
    if 'Password:' in res:
        shell.send(b'huawei@123\n')
