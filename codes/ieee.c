
#include <stdio.h>
#include <string.h>              
#include <stdint.h>              

#define main cprog_recur_main
#include "cprog/codes/prog/recur.c"
#undef main

/* 2^e as a double. power() only handles n >= 0 (it counts n down to 0),
   so a negative exponent is done as 1 / 2^(-e). */
double pow2(int e){
	return (e >= 0) ? power(2, e) : 1.0/power(2, -e);
}

/* IEEE 754 single precision (32 bits):
 *   bit 31      : sign s           (0 = positive, 1 = negative)
 *   bits 30..23 : exponent E       (8 bits, stored with a bias of 127)
 *   bits 22..0  : fraction f       (23 bits)
 *   value = (-1)^s x 1.f x 2^(E - 127)                                   */
int main(){
	uint32_t w = 0xC2710000;           /* the bit pattern from the question */

	/* w >> 31 moves bit 31 to the end, giving the sign bit.
	 * (w >> 23) & 0xFF moves the exponent down and keeps 8 bits (0xFF = 11111111). */
	int s = w >> 31, E = (w >> 23) & 0xFF;
	/* 0x7FFFFF = 23 ones: keeps only the fraction bits */
	uint32_t f = w & 0x7FFFFF;

	/* 1.f = 1 + f / 2^23. Dividing by a double avoids integer division,
	 * which would throw away the fractional part. */
	double mant = 1.0 + f / pow2(23);
	/* Put the three parts into the formula */
	double byhand = (s ? -1 : 1) * mant * pow2(E - 127);

	/* Copy the same 32 bits into a float variable, so the computer's own
	 * floating-point hardware reads them as a number */
	float x;
	memcpy(&x, &w, sizeof x);          /* let the hardware decode it too */

	printf("s = %d, E = %d (e = %d), 1.f = %.7f\n", s, E, E - 127, mant);
	printf("By formula: %.2f\n", byhand);   /* expected -60.25 */
	printf("As float  : %.2f\n", x);        /* same value, as a check */
	return 0;
}
