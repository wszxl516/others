import os
import fcntl
import subprocess


class AsyncPopen(subprocess.Popen):
    def __init__(self, *args, **kwargs):
        super(AsyncPopen, self).__init__(*args, **kwargs)
        self.un_block(self.stderr)
        self.un_block(self.stdout)

    def __iter__(self):
        while True:
            code = self.chk_status()
            if code is not None:
                self.returncode = code
                break
            out = self.stdout.readline()
            err = self.stderr.readline()
            if not out and not err:
                continue
            yield out.decode(), err.decode()

    @staticmethod
    def un_block(fd):
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def chk_status(self):
        _pid, sts = os.waitpid(self.pid, os.WNOHANG)
        code = None
        if _pid == self.pid:
            if os.WIFSIGNALED(sts):
                code = -os.WTERMSIG(sts)
            elif os.WIFEXITED(sts):
                code = os.WEXITSTATUS(sts)
            elif os.WIFSTOPPED(sts):
                code = -os.WSTOPSIG(sts)
            else:
                # Should never happen
                code = 999
        return code


if __name__ == '__main__':
    with AsyncPopen('ping 8.8.8.8 -c 3',
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True)as pro:
        for msg in pro:
            print(msg)
        print('exit: ', pro.returncode)

