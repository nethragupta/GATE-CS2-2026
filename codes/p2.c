/* GATE CS2 2026, Q.19, program P2: error, a redefined in the same scope */
#include <stdio.h>
int main(){
  int a=5;        /* first definition of a in main's block */
  int a=7;        /* ERROR: a second definition of a in the SAME block.
                     gcc reports "redefinition of 'a'". */
  return(0);
}
