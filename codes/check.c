/*
   The condition is d_1 < d_2 < ... < d_{n-1}, where d_i = A[i+1] - A[i].
   Each difference is compared only with the one before it, so a single
   pass through the array is enough: the time taken is Theta(n). */
#include <stdio.h>
#include <stdlib.h>              
#include "cprog/codes/data/libs/datafun.h"

/* returns 1 if d_1 < d_2 < ... < d_{n-1}, d_i = A[i+1] - A[i] */
int check(int A[], int n){
	/* The n-1 differences, in an array made with cprog's createVec */
	int *d = createVec(n - 1);
	for (int i = 0; i + 1 < n; i++) d[i] = A[i+1] - A[i];   /* first pass: n-1 subtractions */
	printf("differences: ");
	printData(d, n - 1);                     /* show them */
	printf("\n");

	/* The later difference must be strictly bigger than the one before it */
	int ok = 1;
	for (int i = 1; i < n - 1; i++)          /* second pass: n-2 comparisons */
		if (d[i] <= d[i-1]) { ok = 0; break; }   /* stop at the first failure */
	free(d);                                 /* give back the memory */
	return ok;                               /* two passes: still Theta(n) */
}

int main(){
	/* Two test arrays of 6 elements each */
	int A[] = {1, 2, 4, 7, 11, 16};       /* differences 1,2,3,4,5 */
	int B[] = {1, 3, 4, 7, 11, 16};       /* differences 2,1,...   */
	printf("A satisfies the condition: %d\n", check(A, 6));   
	printf("B satisfies the condition: %d\n", check(B, 6));   
	return 0;
}
