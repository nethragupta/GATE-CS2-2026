
#include <stdio.h>
#include <stdlib.h>             
#include "cprog/codes/data/libs/datafun.h"


#define main cprog_recur_main
#include "cprog/codes/prog/recur.c"
#undef main

#define NEL 5                    /* number of elements */

int main(){
	int target[NEL] = {4, 3, 1, 2, 5};          /* output we want */
	/* S, Q = arrays used as stack and queue; out = the output sequence */
	int *S = createVec(NEL), *Q = createVec(NEL), *out = createVec(NEL);
	/* mask is a 5-bit number; each bit says where one element goes */
	for (int mask = 0; mask < power(2, NEL); mask++){   /* bit i set: element i+1 -> S */
		/* ns, nq = how many S and Q hold; k = length of out so far
		 * ok stays 1 while out matches target */
		int ns = 0, nq = 0, k = 0, ok = 1;
		for (int e = 1; e <= NEL; e++){
			/* (1 << (e - 1)) has only bit e-1 set; "&" tests that bit of mask */
			if (mask & (1 << (e - 1))) S[ns++] = e;  /* push */
			else Q[nq++] = e;                        /* enqueue */
		}
		/* Stack: last in, first out, so pop from the top (S[--ns]) */
		while (ns > 0) out[k++] = S[--ns];          /* pop all */
		/* Queue: first in, first out, so read from the front */
		for (int i = 0; i < nq; i++) out[k++] = Q[i];  /* dequeue all */
		for (int i = 0; i < NEL; i++) if (out[i] != target[i]) ok = 0;
		if (ok){
			/* Print the assignment, e.g. "1Q 2Q 3S 4S 5Q", then the output */
			for (int e = 1; e <= NEL; e++) printf("%d%c ", e, (mask & (1 << (e - 1))) ? 'S' : 'Q');
			printf("-> output ");
			printData(out, NEL);
			printf("\n");
		}
	}
	free(S); free(Q); free(out);                /* give back the memory */
	return 0;
}
