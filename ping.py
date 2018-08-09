#!/usr/bin/python3
import os
import sys
import socket
import struct
import select
import time


class Icmp:
    def __init__(self, host, time_out=2, count=1, interval=1):
        self._host = host
        self._time_out = time_out
        self._count = count
        self._pid = os.getpid()
        self._interval = interval
        icmp_pro = socket.getprotobyname('icmp')
        self._socks = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_pro)

    def start(self):
        response = []
        try:
            for _ in range(self._count):
                ip = self.send()
                delay = self.recv()
                response.append((round(delay*1000*1000, 4) if delay else None, ip))
                time.sleep(self._interval)
            return response
        except socket.gaierror as e:
            print("failed. (socket error: '%s')" % e[1])
            return None
        finally:
            self._socks.close()

    def send(self):
        ip = socket.gethostbyname(self._host)
        header = struct.pack('bbHHh', 8, 0, 0, self._pid, 1)
        byte_in_double = struct.calcsize("d")
        data = (192 - byte_in_double) * "P"
        data = struct.pack("d", time.clock()) + data.encode()
        my_checksum = self.checksum(header + data)
        header = struct.pack("bbHHh", 8, 0, socket.htons(my_checksum), self._pid, 1)
        packet = header + data
        self._socks.sendto(packet, (ip, 80))
        return ip

    def recv(self):
        start_time = self._time_out
        start_select = time.time()
        wait_ready = select.select([self._socks], [], [], start_time)
        how_long = (time.time() - start_select)
        if not wait_ready[0]:
            return

        while True:
            time_received = time.clock()
            rec_packet, addr = self._socks.recvfrom(1024)
            icmp_header = rec_packet[20: 28]
            ip_type, code, check_sum, packet_id, sequence = struct.unpack("bbHHh", icmp_header)
            if ip_type != 8 and packet_id == self._pid:
                byte_in_double = struct.calcsize("d")
                time_sent = struct.unpack("d", rec_packet[28: 28 + byte_in_double])[0]
                return time_received - time_sent

            start_time = start_time - how_long
            if start_time <= 0:
                return

    @staticmethod
    def checksum(source):
        check_sum = 0
        count = (len(source) / 2) * 2
        i = 0
        while i < count:
            temp = source[i + 1] * 256 + source[i]
            check_sum = check_sum + temp
            check_sum = check_sum & 0xffffffff
            i = i + 2

        if i < len(source):
            check_sum = check_sum + source[len(source) - 1]
            check_sum = check_sum & 0xffffffff

        check_sum = (check_sum >> 16) + (check_sum & 0xffff)
        check_sum = check_sum + (check_sum >> 16)
        answer = ~check_sum
        answer = answer & 0xffff

        answer = answer >> 8 | (answer << 8 & 0xff00)
        return answer


if __name__ == '__main__':
    try:
        cmd = sys.argv[1]
        if not cmd:
            sys.exit()
        icmp = Icmp(cmd, time_out=3, count=10, interval=0.1)
        print(icmp.start())
    except EOFError:
        pass
    except PermissionError as error:
        print('Only run as root!')
    except KeyboardInterrupt as error:
        pass
