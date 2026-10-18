/*
   Method: append r = (generator length - 1) zeros to the data, then do
   modulo-2 long division (subtraction is XOR, no borrows). The last r bits
   left over are the CRC remainder. Each bit is stored as an int 0 or 1. */
#include <stdio.h>
#include <stdlib.h>              /* malloc, free */
#include "cprog/codes/data/libs/datafun.h"

int main(){
	int data[] = {1, 1, 0, 0, 0, 1, 0, 1, 1};     /* 110001011 */
	int gen[]  = {1, 0, 0, 1};                    /* 1001 */
	int n = sizeof(data)/sizeof(data[0]);         /* 9 data bits */
	int r = sizeof(gen)/sizeof(gen[0]) - 1;       /* 3 = degree of the generator */

	/* buf = data followed by r zeros: the working space for the division */
	int *buf = createVec(n + r);
	for (int i = 0; i < n; i++) buf[i] = data[i];
	for (int i = 0; i < r; i++) buf[n + i] = 0;   /* append r zeros */

	/* Long division: move along the data bits. Whenever the leading bit
	 * is 1, XOR the generator into buf starting at that bit. */
	for (int i = 0; i < n; i++){                        /* modulo-2 division */
		if (buf[i] == 1){
			for (int j = 0; j <= r; j++)
				buf[i + j] ^= gen[j];     /* ^ is XOR: equal bits give 0, different give 1 */
			printData(buf, n + r);        /* show buf after each step */
			printf("\n");
		}
	}
	/* buf + n points at the last r bits: the remainder (expected 1 0 0) */
	printf("Remainder = ");
	printData(buf + n, r);
	printf("\n");
	free(buf);                                    
	return 0;
}
