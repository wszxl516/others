#!/usr/local/bin/python3
import subprocess as sub
import os
import shutil
def cmd(args):
    pro = sub.Popen(args=args,bufsize=1024,stdout=sub.PIPE,stderr=sub.PIPE,shell=True)
    res = [i.decode() for i in pro.stdout.readlines()]
    return res
def copy(filelist, topath):
    for f in filelist:
        fpath = os.path.split(f)[0]
        to_path = os.path.join(topath,fpath[1:])
        if not os.path.exists(to_path):
            print('directory <%s> is not exists create it!'% to_path)
            os.makedirs(to_path)
        print(os.path.join(topath,f[1:]))
        shutil.copyfile(f,os.path.join(topath,f[1:]))
def main():
    all = []
    with open('binlist.txt', 'r')as fp:
        files = [i.strip() for i in fp.readlines()]
    for binf in files:
        binpath = cmd('which %s'%binf)
        try:
           bin = binpath[0].strip()
        except Exception as e:
           print(binf, 'is not exists!')
           continue
        allso = cmd('ldd %s'% bin)
        for i in allso:
            for s in i.split():
                all.append(s)
        all.append(bin)
    all = [i for i in all if os.path.exists(i)]
    all = list(set(all))
    copy(all, '/mnt/sysroot')
    return all
if __name__ == '__main__':
    main()
