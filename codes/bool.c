/*
   Method: build the truth table of F as a vector of 16 values, then for
   each option build a vector "agree" with 1 on every row where the option
   equals F. The option is correct only if sum(agree) = 16 (all rows). */
#include <stdio.h>
#include <stdlib.h>              


#define main cprog_filesfunc_main
#include "cprog/codes/prog/fileprogs/filesfunc.c"
#undef main
#define main cprog_recur_main
#include "cprog/codes/prog/recur.c"
#undef main

int main(){
	int rows = power(2, 4);              /* 4 inputs A, B, C, D: 2^4 = 16 rows */

	/* F[m] = value of F on input number m (0 to 15), all 0 to begin with */
	int *F = createVec(rows);
	for (int m = 0; m < rows; m++) F[m] = 0;
	/* The minterms of F, i.e. the inputs where F = 1 */
	int list[] = {0, 1, 2, 3, 8, 9, 10, 11};
	for (int k = 0; k < 8; k++) F[list[k]] = 1;   /* mark them as 1 */

	const char *name[4] = {"i)   A'+B'+C'+D'", "ii)  B'", "iii) A'B'+AB", "iv)  A'"};
	int *agree = createVec(rows);
	for (int o = 0; o < 4; o++){
		for (int m = 0; m < rows; m++){
			/* Split m into its 4 bits: A is the most significant bit, D the least.
			 * (m >> 3) shifts m right by 3 places; "& 1" keeps only the last bit.
			 * Example: m = 9 = 1001 in binary gives A=1, B=0, C=0, D=1. */
			int A = (m >> 3) & 1, B = (m >> 2) & 1, C = (m >> 1) & 1, D = m & 1;

			/* Value of each option on this row.*/
			int opt[4] = { !A || !B || !C || !D,      /* i)   A'+B'+C'+D' */
			               !B,                        /* ii)  B'          */
			               (!A && !B) || (A && B),    /* iii) A'B' + AB   */
			               !A };                      /* iv)  A'          */
			agree[m] = (opt[o] == F[m]);              /* 1 if this row agrees */
		}
		/* sum() adds up the vector: the number of rows where option o equals F.
		 * %-18s prints the name left-aligned in 18 characters. */
		int n_agree = sum(agree, rows);
		printf("%-18s agrees on %2d of %d rows: %s\n", name[o], n_agree, rows,
		       n_agree == rows ? "matches F" : "does not match");
	}
	/* Expected: only ii) B' matches, since every minterm of F has B = 0 */
	free(F); free(agree);                         
	return 0;
}
