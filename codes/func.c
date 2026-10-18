#include <stdio.h>
#include <stdlib.h>             
#include "cprog/codes/data/libs/datafun.h"

/* Recursive function from the question.
 * length = number of positions from start to end (inclusive).
 * Each call shrinks the range, so the recursion always ends. */
int func(int start, int end){
    int length=end+1-start;

    /* Base case: empty range or negative index -> stop and return 0 */
    if((length<1)||(start<0)||(end<0)){ return(0); }

    if(length%3==0){
        /* length = 0 (mod 3): drop the first position, add nothing.
         * New length = length - 1, which is 2 (mod 3). */
        return(func(start+1, end));
    } else if(length%3==1){
        /* length = 1 (mod 3): drop the last position and ADD 1.
         * New length = length - 1, which is 0 (mod 3).
         * This is the only branch that increases the result. */
        return(1+func(start, end-1));
    } else {
        /* length = 2 (mod 3): drop the first two positions, add nothing.
         * New length = length - 2, which is 0 (mod 3). */
        return(func(start+2, end));
    }
    /* After the first call, the length is always 0 or 2 (mod 3) and never
     * 1 (mod 3) again, so the "+1" branch can run at most once.
     * Hence the maximum possible value is 1. */
}

#define LO -5                    /* smallest start/end tried (negative checks the base case) */
#define HI 300                   /* tries values up to HI - 1 = 299 */

int main(){
	int side = HI - LO;              /* 305 values for start, and for end */
	int n = side*side;               /* number of (start, end) pairs */
	/* vals[k] = func value for pair number k, in an array made with cprog's createVec */
	int *vals = createVec(n);
	int k = 0;
	for (int s = LO; s < HI; s++)
		for (int e = LO; e < HI; e++)
			vals[k++] = func(s, e);  /* value for this pair */

	/* max() returns the largest value in the array */
	int best = max(vals, n);

	/* Find the first pair that reaches it: pair k has
	 * start = LO + k / side and end = LO + k % side */
	for (k = 0; vals[k] != best; k++);
	int bs = LO + k / side, be = LO + k % side;

	/* Expected output: Maximum value = 1 (first reached at func(0, 0)) */
	printf("Maximum value = %d (first reached at func(%d, %d))\n", best, bs, be);
	free(vals);                      /* give back the memory */
	return 0;
}
