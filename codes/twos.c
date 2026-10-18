/*
   An n-bit two's complement number can hold -2^(n-1) to 2^(n-1) - 1,
   i.e. -8 to 7 for n = 4. Overflow happens when the true result of an
   operation is outside that range. */
#include <stdio.h>
#define main cprog_recur_main
#include "cprog/codes/prog/recur.c"
#undef main

#define NBITS 4                  /* word size in the question */

/* value of a 4-bit two's complement pattern */
int val4(int bits){
	/* The sign bit is the top bit, worth 2^(n-1) = 8. If it is set, the
	 * number is negative: value = pattern - 2^n.
	 * Example: 1011 = 11, so its value is 11 - 16 = -5. */
	return (bits & power(2, NBITS - 1)) ? bits - power(2, NBITS) : bits;
}

/* Print a result and say whether it fits in NBITS bits */
void check(const char *name, int x){
	int lo = -power(2, NBITS - 1), hi = power(2, NBITS - 1) - 1;   /* -8 and 7 */
	printf("%-12s = %3d  %s\n", name, x, (x < lo || x > hi) ? "OVERFLOW" : "ok");
}

int main(){
	/* 0xB = 1011, 0xD = 1101, 0xA = 1010, 0x9 = 1001 (hexadecimal = 4 bits each) */
	int N1 = val4(0xB), N2 = val4(0xD), N3 = val4(0xA), N4 = val4(0x9);
	printf("N1 = %d, N2 = %d, N3 = %d, N4 = %d, range [%d, %d]\n",
	       N1, N2, N3, N4, -power(2, NBITS - 1), power(2, NBITS - 1) - 1);
	/* Expected: ii) and iv) overflow */
	check("i)   N1+N2", N1 + N2);
	check("ii)  N2+N3", N2 + N3);
	check("iii) N3-N4", N3 - N4);
	check("iv)  N1+N4", N1 + N4);
	return 0;
}
