#include <stdio.h>  
#include <unistd.h>  
#include <string.h>
#define _XOPEN_SOURCE  
  
int main(int args, char **argv)  
{  
        char *passwd;  
        char salt[20]={};
        strcat(salt,"$6$");
        strcat(salt,argv[2]);
        passwd = crypt(argv[1], salt);  
        printf("%s\n", passwd);  
        return 0;  
}
