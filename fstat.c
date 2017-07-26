#include <sys/stat.h>  
#include <fcntl.h>  
#include "stdio.h"  
#include "time.h"  
#include "unistd.h"  
#include "malloc.h"
void report(struct stat *ptr)  
{  
    if(!ptr)  
    {  
           return;  
       }  
          
    printf("设备号：%lu\n", ptr->st_dev);  
    printf("所在节点: %lu\n", ptr->st_ino);  
    printf("文件属性: %o\n", ptr->st_mode);  
    printf("链接数: %lu\n", ptr->st_nlink);  
    printf("所属用户: %d\n", ptr->st_uid);  
    printf("属组: %d\n", ptr->st_gid);  
    printf("文件大小: %ld\n", ptr->st_size);  
    printf("文件块大小: %ld\n", ptr->st_blksize);  
    printf("文件块数量: %ld\n", ptr->st_blocks);   
    struct tm* pAccesstime=localtime(&(ptr->st_atime));  
    struct tm* pModifytime=localtime(&(ptr->st_mtime));  
    struct tm* pChangetime=localtime(&(ptr->st_ctime));  
    char aBuffer[64] = {0};  
    char mBuffer[64] = {0};  
    char cBuffer[64] = {0};  
    strftime(aBuffer, 64, "最后访问: %Y-%m-%d %H:%M:%S \n", pAccesstime);  
    strftime(mBuffer, 64, "数据修改: %Y-%m-%d %H:%M:%S \n", pModifytime);  
    strftime(cBuffer, 64, "节点修改: %Y-%m-%d %H:%M:%S \n", pChangetime);  
  
    printf("%s",aBuffer);  
    printf("%s",mBuffer);  
    printf("%s",cBuffer);  
}  
  
void Test(const char* pFileName)  
{  
    if(!pFileName)  
    {  
           printf("请输入文件名\n");  
           return;  
       }  
  
    struct stat st;  
    int nRev_st = stat(pFileName, &st);  
    if(nRev_st < 0)  
    {  
           printf("文件%s 不存在。\n", pFileName);  
       }  
    else  
    {  
           report(&st);  
       }  
 /* 
    struct stat ls;  
    int nRev_ls = lstat(pFileName, &ls);  
    if(nRev_ls < 0)  
    {  
           printf("File %s is not existed \n", pFileName);  
       }  
    else  
    {  
           printf("------get file %s info by lstat \n", pFileName);  
           report(&ls);  
       }  
  
    struct stat fs;  
    int fd = open(pFileName, O_RDONLY);  
    int nRev_fs = fstat(fd, &fs);  
    close(fd);  
    if(nRev_fs < 0)  
    {  
           printf("File %s is not existed \n", pFileName);  
       }  
    else  
    {  
           printf("------get file %s info by fstat \n", pFileName);  
           report(&fs);  
       }  
       */
}  
  
int main(int argv, char *args[])  
{  
    const char* pFileName_Real = args[1];  
    Test(pFileName_Real);  
    printf("\n\n");  
    return 0;  
}  
