#include <math.h>
#include <stdio.h>
#include <string.h>
int main(int argv, char *args[])
{
char *str ;
str = args[1];
double num=0;
double i,x;
int len = (int)strlen(str);
for(i = 0; i<len;i++)
{
    x = str[(int)i] - 48;
    num += x * pow(10,len-i-1);
}
printf("%d\n",(int)num);
return (int)num;
}
