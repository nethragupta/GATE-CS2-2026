/* GATE CS2 2026, Q.60: program from the question */
#include <stdio.h>
int main(){
    int *ptr, a, b, c;        /* ptr is a pointer: it stores the address of an int */
    a=5; b=11; c=20;
    ptr=&a;                   /* &a = address of a, so ptr now points to a     */
    *ptr=c;                   /* *ptr is "the int ptr points to" = a, so a = 20 */
    ptr=&c;                   /* ptr now points to c                            */
    a=*(&b);                  /* *(&b) is just b, so a = 11                     */
    c=*ptr-a;                 /* *ptr is c = 20, so c = 20 - 11 = 9             */
    printf("%d",c);           /* prints 9 */
    return(0);
}
