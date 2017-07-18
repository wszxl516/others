#!/usr/bin/python3
import os
import sys
import socket
import struct
import select
import time
import ctypes


def recv(my_socket, ID, timeout):
    start_time = timeout
    while True:
        start_select = time.clock()
        what_ready = select.select([my_socket], [], [], start_time)
        how_long = (time.clock() - start_select)
        if what_ready[0] == []:
            return

        time_received = time.clock()
        rec_packet, addr = my_socket.recvfrom(1024)
        icmp_header = rec_packet[20 : 28]
        ip_type, code, checksum, packet_ID, sequence = struct.unpack("bbHHh", icmp_header)
        if ip_type != 8 and packet_ID == ID:
            byte_in_double = struct.calcsize("d")
            time_sent = struct.unpack("d", rec_packet[28 : 28 + byte_in_double])[0]
            return time_received - time_sent

        start_time = start_time - how_long
        if start_time <= 0:
            return


def checksum(source):
    checksum = 0
    count = (len(source) / 2) * 2
    i = 0
    while i < count:
        temp = source[i + 1] * 256 + source[i]
        checksum = checksum + temp
        checksum = checksum & 0xffffffff
        i = i + 2

    if i < len(source):
        checksum = checksum + source[len(source) - 1]
        checksum = checksum & 0xffffffff

    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = checksum + (checksum >> 16)
    answer = ~checksum
    answer = answer & 0xffff

    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def send(my_socket, ip_addr, ID):
    ip = socket.gethostbyname(ip_addr)
    print(ip)
    my_checksum = 0
    header = struct.pack('bbHHh', 8, 0, 0, ID, 1)
    byte_in_double = struct.calcsize("d")
    data = (192 - byte_in_double) * "P"
    data = struct.pack("d", time.clock()) + data.encode()
    my_checksum = checksum(header + data)
    header = struct.pack("bbHHh", 8, 0, socket.htons(my_checksum), ID, 1)
    packet = header + data
    my_socket.sendto(packet, (ip, 80))

def icmp(ip_addr, timeout = 2):
    try:
        icmp = socket.getprotobyname('icmp')
        try:
            socks = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        except socket.error:
            raise
        ID = os.getpid() & 0xFFFF
        send(socks, ip_addr, ID)
        delay = recv(socks, ID, timeout)
        socks.close()
    except socket.gaierror as e:
        print("failed. (socket error: '%s')" % e[1])
        return None
    if delay == None:
        print('failed. (timeout within %s second.)' % timeout)
        return None
    else:
        print('reply in %0.4f ms' % (delay * 1000))


if __name__ == '__main__':
    try:
        cmd = sys.argv[1]
        if not cmd:
            sys.exit()
        icmp(cmd)
        time.sleep(1)
    except EOFError:
        pass
    except PermissionError as error:
        print('Only run in root!')
    except KeyboardInterrupt as error:
        pass