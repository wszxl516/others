
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
    so.pfree.argstypes = ct.POINTER(StructPointer)
    so.pfree(StructPointer)
#C代码
'''
#include <stdio.h>  
#include <string.h>  
#include <stdlib.h>  
  
typedef struct StructPointerTest  
{  
    char name[20];  
    int age;  
}StructPointerTest, *StructPointer;  
  
StructPointer test()    // 返回结构体指针  
{   
    StructPointer p = (StructPointer)malloc(sizeof(StructPointerTest));   
    strcpy(p->name, "Joe");  
    p->age = 20;  
      
    return p;   
}  
void pfree(StructPointer p)
{
free(p);
}

'''
