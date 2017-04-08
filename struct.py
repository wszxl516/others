
#!/usr/local/bin/python3
import ctypes as ct
class StructPointer(ct.Structure):
    _fields_ = [("name", ct.c_char * 20), ("age",ct.c_int)]
if __name__ == '__main__':
    so = ct.cdll.LoadLibrary('./test.so')
    so.test.restype = ct.POINTER(StructPointer)
    res = so.test()
    print (res.contents.name)
    print (res.contents.age)
