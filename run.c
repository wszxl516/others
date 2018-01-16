#include <Python.h>

int main()

{

    Py_Initialize();                             
    PyObject * pModule = NULL;    //声明变量  
    PyObject * pFunc = NULL;      //声明变量 
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./')");     
    pModule =PyImport_ImportModule("ip");
    if (!pModule)
    {
     printf("can't find module!");
     return -1;
    }
    pFunc= PyObject_GetAttrString(pModule, "main");
    PyEval_CallObject(pFunc, NULL);  
    Py_Finalize();                          

    return 0;

}
