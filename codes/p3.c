/* GATE CS2 2026, Q.19, program P3: error, conflicting types for a */
#include <stdio.h>
int main(){
  int a=5;        /* a defined as an int in main's block */
  float a=7;      /* ERROR: a defined again in the SAME block, now as a float.
                     gcc reports "conflicting types for 'a'". */
  return(0);
}
