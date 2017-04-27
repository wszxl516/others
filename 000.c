#include <string.h>
#include <stdio.h>
#include <unistd.h>
void getinfo(int *num);
float meminfo();
int main(void)
{
float mem=0.0;
int num[8];
getinfo(num);
mem = meminfo();
printf("%2.2f%% \n",mem);
return 0;
}

void getinfo(int *num)
{
char temp[128], tmp='\0', *tt;
FILE *fp=NULL;
int i=0;
fp = fopen("/proc/stat", "r");
printf("read file!");
while(tmp!=10)
{
    fread(&tmp,1,1,fp);
    temp[i]=tmp;
    printf("temp[i] %s\n",temp[i]);
    i++;
}
fclose(fp);
}
float meminfo()
{
char total[10],free[10], tmp, t;
FILE *fp=NULL;
int all=0,used=0,i=0;
fp = fopen("/proc/meminfo", "r");
if(fp == NULL)
printf("file not exist!");
while(tmp!=10)
{
    fread(&tmp,1,1,fp);
    if((int)tmp>=48&&(int)tmp<=57)
    {
       total[i]=tmp;
       i++;
    }

}
all = atoi(total);
i = ftell(fp);
fseek(fp,i,0);
i = 0;
while(t!=10)
{
fread(&t,1,1,fp);
if((int)t>=48&&(int)t<=57)
{
    free[i]=t;
    i++;
}
}
used = atoi(free);

return 100*(all-used)/all;
}
