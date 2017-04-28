#include <signal.h>  
#include <stdlib.h>  
#include <stdio.h>  
#include <unistd.h>  
  
void my_handler(int s){  
           printf("exit %d\n",s);  
           exit(1);   
  
}  
  
int main(int argc,char** argv)  
{  
  
   struct sigaction sig;  
  
   sig.sa_handler = my_handler;  
   sigemptyset(&sig.sa_mask);  
   sig.sa_flags = 0;  
  
   sigaction(SIGINT, &sig, NULL);  
  
   pause();  
  
   return 0;      
} 

