#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
void getdata(int *all);
float meminfo();
float getinfo(); 
void stop(int stopsignal);
int main(void)
{
float mem=0.0,cpu=0.0;
struct sigaction sig;
sig.sa_handler = stop;
sigemptyset(&sig.sa_mask);
sig.sa_flags = 0;
sigaction(SIGINT, &sig, NULL);
while(1)
{
    cpu = getinfo();
    mem = meminfo();
    printf("\33\[K\33\[s\33\[1m\33\[?25l\33\[37mCPU:\33\[32m%6.2f%%\33\[37m MEM:\33\[32m%6.2f%%\33\[32m\33\[u",cpu,mem);
    fflush(stdout);
}

return 0;
}
void stop(int stopsignal)
{

    printf("\33\[?25h\33\[0m\33\[K\n");
    exit(0);
}

float getinfo()
{
int all1[10],all[10],i;
int total=0,user=0;
getdata(all);
sleep(1);
getdata(all1);
for(i=0;i<8;i++)
{
    total += all1[i] - all[i];
    if(i<3)
    {
        user += all1[i] - all[i];
    }

}
return (float)(user*100)/(float)(total);
}

void getdata(int *all)
{
char temp[10][10]={0},tmp='\0';
int i = 0,x = 0;
FILE *fp=NULL;
int size=0;
int flag=0;
fp = fopen("/proc/stat", "r");
while(tmp!=10)
{
    tmp = fgetc(fp);
    if(tmp>=48&&tmp<=57)
    {
        temp[i][x] = tmp;
        flag = 1;
        x++;
    }
    if(tmp == 32 && flag)
    {
        x = 0;
        flag = 0;
        all[i] = atol((const char*)&temp[i]);
        i++;
    }
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
    tmp = fgetc(fp);
    if(tmp>=48&&tmp<=57)
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
t = fgetc(fp);
if((int)t>=48&&(int)t<=57)
{
    free[i]=t;
    i++;
}
}
 used = all - atoi(free);
return 100*used/all;
}
