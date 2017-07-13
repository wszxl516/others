#include <unistd.h>
#include <stdio.h>
#include <malloc.h>
typedef struct Node{
int num;
struct Node *next;

}NODE, *PNODE;
typedef struct Stack{
PNODE top;
PNODE btm;
}STACK ,*PSTACK;

int init(PSTACK ps);
void push(PSTACK ps, int var);
void traverse(PSTACK ps);
void pop(PSTACK ps);
void clear(PSTACK ps);
int empty(PSTACK ps);
int main(int argc, char *args)
{
STACK ss;
if(init(&ss)) printf("init success!\n");
else 
{
    printf("init failed!\n");
    return 1;
}
for(int i=0;i<10;i++)
{
    push(&ss,i);
}
traverse(&ss);
clear(&ss);
traverse(&ss);
/*for test
for(int i=0;i<10;i++)
{
PNODE p=pop(&ss);
printf("%d\n", p->num);
}
traverse(&ss);
*/
return 0;
}


int init(PSTACK ps)
{
ps->top = (PNODE) malloc(sizeof(PNODE));
if(ps->top == NULL) //申请内存是否失败
{
    return 0;
}
else
{
    ps->btm = ps->top;//只有一个节点
    ps->top->next = NULL;
    ps->top->num = 0;
    return 1;

}
}
void push(PSTACK ps, int var)
{
PNODE pnew = (PNODE) malloc(sizeof(PNODE));
pnew->num = var;
pnew->next = ps->top;//新节点next为当前栈顶
ps->top = pnew;//新节点为栈顶

}

void traverse(PSTACK ps)
{
if(empty(ps))
{
    printf("this STACK is empty!\n");
    return;
}
PNODE p = ps->top;
while(p != ps->btm)//未到栈底遍一直循环
{
    printf("%d\n", p->num);
    p = p->next;//指向当前节点的下一个节点

}
}
int empty(PSTACK ps)
{
if(ps->top == ps->btm)
{
    return 1;
}
else
{
    return 0;
}
}

void pop(PSTACK ps)
{
if(empty(ps))
{
    return ;
}
PNODE tmp = ps->top;//保存需要释放的指针
free(tmp);
ps->top = ps->top->next;//栈顶指向下一个节点
return ;


}
void clear(PSTACK ps)
{
PNODE p = ps->top;
PNODE n = NULL;
while(p !=ps->btm)//检测是否为栈底
{
    n = p->next;//指向下一节点
    free(p);//释放
    p = n;

}
ps->top = ps->btm;//首节点指向末尾表示为空
}
