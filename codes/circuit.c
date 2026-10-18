/*
   The circuit: a 2:4 decoder with inputs A, B feeds a 4:1 multiplexer
   with select lines S1, S0. Mux inputs: I0 = D0, I1 = 0, I2 = 1, I3 = D3.
   Method: store Y for all 2^4 = 16 inputs in a vector; the number of
   combinations with Y = 1 is the sum of that vector. */
   
#include <stdio.h>
#include <stdlib.h>              


#define main cprog_filesfunc_main
#include "cprog/codes/prog/fileprogs/filesfunc.c"
#undef main
#define main cprog_recur_main
#include "cprog/codes/prog/recur.c"
#undef main

int main(){
	int rows = power(2, 4);              /* 4 inputs: 2^4 = 16 rows */
	int *Yvec = createVec(rows);         /* Y for each row */
	printf(" A B S1 S0 | Y\n");          /* heading of the truth table */
	for (int m = 0; m < rows; m++){
		/* Split m into 4 bits: A is the most significant, S0 the least */
		int A = (m >> 3) & 1, B = (m >> 2) & 1, S1 = (m >> 1) & 1, S0 = m & 1;

		/* Decoder: output D_k is 1 only when the input AB equals k in binary.
		 * D0 = A'B' (AB = 00),  D3 = AB (AB = 11) */
		int D0 = !A && !B, D3 = A && B;          /* 2:4 decoder outputs used */

		/* Multiplexer: its output is the input chosen by the select lines */
		int I[4] = {D0, 0, 1, D3};               /* multiplexer inputs       */
		Yvec[m] = I[2*S1 + S0];                  /* S1 S0 in binary = 2*S1 + S0 */

		printf(" %d %d  %d  %d | %d\n", A, B, S1, S0, Yvec[m]);   /* one row of the table */
	}
	/* Expected: 1 (from I0) + 0 (I1) + 4 (I2) + 1 (I3) = 6 */
	printf("Combinations with Y = 1: %d\n", sum(Yvec, rows));
	free(Yvec);                          /* give back the memory */
	return 0;
}
