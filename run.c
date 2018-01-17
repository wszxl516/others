#include <Python.h>

int main(int argc, char **argv)
{

    int ret;
    Py_Initialize();                             
    PyObject * pModule = NULL; 
    PyObject * pFunc = NULL;  
    PyObject * pArgs = NULL;
    PyObject * pResult = NULL;
    if(argc > 1)
    {
        pArgs = PyTuple_New(argc);
        for(int i=1;i<argc;i++)
        {
             PyTuple_SetItem(pArgs,i-1,Py_BuildValue("s", argv[i]));
             printf("%s\n", argv[i]);
         }   
    }
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./')");     
    pModule =PyImport_ImportModule("test_run");
    if (pModule == NULL)
    {
        printf("Can't find module test_run!");
        return -1;
    }
    pFunc= PyObject_GetAttrString(pModule, "test");
    if (pFunc == NULL)
    {
        printf("Can't find function test!");
        return -1;
    }
    printf("pArgs is %p\n",pArgs);
    pResult = PyEval_CallObject(pFunc, pArgs);  
    PyArg_Parse(pResult, "i", &ret);
    printf("result = %d\n", ret);
    Py_Finalize();                          
    return 0;

}
