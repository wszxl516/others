#!/usr/bin/python
# encoding = utf-8
import Time

class Time:
    def __init__(self, hour, minute, second):
        self._h = hour
        self._m = minute
        self._s = second
    def __add__(self, other):
        self._s += other._s
        if self._s > 60:
            self._s -= 60
            self._m += 1
        self._m += other._m
        if self._m > 60:
            self._m -= 60
            self._h += 1
        self._h += other._h
        if self._h > 24:
            self._h -= 24
    def __sub__(self, other):
        self._h -= other._h
        if self._m < other._m:
            self._h -= 1
            self._m -= other._m-60
        else:
            self._m -= other._m
        if self._s < other._s:
            self._m -= 1
            self._s -= other._s-60
        else:
            self._s -= other._s
    def __str__(self):
        return '{0}:{1}:{2}'.format(self._h, self._m, self._s)


a = Time(11, 22, 33)
b = Time(5, 44, 33)
print a
print b
b-a
print b
