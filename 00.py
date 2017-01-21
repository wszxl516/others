import subprocess as subpro
def run(cmd):
    pro = subpro.Popen(cmd,bufsize=1024, stdout=subpro.PIPE, stderr=subpro.PIPE, shell=False, env={"PATH": "/system/bin:/bin"})
    while pro.stdout.readable():
        print(pro.stdout.readline().decode())
    while pro.stderr.readable():
        print("ERROR:")
        print(pro.stderr.read())
run(['ping', 'baidu.com'])
