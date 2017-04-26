
#include <string.h>
#include <stdio.h>
#include <unistd.h>
void getinfo(int *user, int *all);

int main(void)
{
int u1=0,u2=0,a1=0,a2=0;
int percent=0;
getinfo(&u1,&a1);
printf("%d -- %d",u1,a1);
sleep(1);
getinfo(&u2,&a2);
printf("%d -- %d",u2,a2);
percent = 100*(u2-u1)/(a2-a1);
printf("User: %d All: %d Percent: %d",u1,a1,percent);
return 0;
}
void getinfo(int *user, int *all)
{
char temp[256]="\0", tmp[1]="\0";
int num[8];
FILE *fp=NULL;
int i=0;
int a=0,u=0;
fp = fopen("/proc/stat", "r");
if(fp == NULL)
printf("file not exist!");
while(strcmp(tmp,"\n")!=0)
{
    fread(tmp,1,1,fp);
    strcat(temp,tmp);
}
fclose(fp);
strtok(temp, " ");
for(i;i<8;i++)
{
    num[i] = atoi(strtok(NULL, " "));
    a += num[i];
    if(i<3) u += num[i];
}
*all = a, *user=u;
printf("User: %d All: %d",u,a);
}
