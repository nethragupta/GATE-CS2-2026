/* GATE CS2 2026, Q.19, program P1: compiles (local a hides global a) */
#include <stdio.h>
int a=5;          /* global a: file scope, visible everywhere in this file */
int main(){
  int a=7;        /* local a: block scope, inside main only.
                     A different scope from the global one, so this is allowed;
                     inside main, "a" now means this local a (it hides the global). */
  return(0);      /* compiles and runs with no error */
}
