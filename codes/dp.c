/*
   Recursion: T[i][j] = 1 if i = 0 or j = 0, else 2 T[i-1][j] + 3 T[i][j-1].
   An algorithm is correct if, when it computes T[i][j], both T[i-1][j]
   (cell above) and T[i][j-1] (cell to the left) are already computed.
   Method: fill the table with B1 and with B2, and compare both with the
   value given by the recursion itself. */
#include <stdio.h>
#define N 8                       /* table size: indices 0 to N */

/* R  = reference values from the recursion
 * T1 = table filled by algorithm B1
 * T2 = table filled by algorithm B2 */
long long R[N+1][N+1], T1[N+1][N+1], T2[N+1][N+1];

/* reference: the recursive formulation itself, evaluated directly */
long long rec(int i, int j){
	if (i == 0 || j == 0) return 1;          /* base case: first row or column */
	return 2*rec(i-1, j) + 3*rec(i, j-1);
}

int main(){
	int i, j, s, ok1 = 1, ok2 = 1;           /* ok1, ok2 become 0 on any mismatch */

	/* Start every cell at 1: this sets the base cases (row 0, column 0) */
	for (i = 0; i <= N; i++) for (j = 0; j <= N; j++) R[i][j] = T1[i][j] = T2[i][j] = 1;
	for (i = 0; i <= N; i++) for (j = 0; j <= N; j++) R[i][j] = rec(i, j);

	/* Algorithm B1: row by row, left to right.
	 * The row above (i-1) and the cell to the left (j-1) are done first. */
	for (i = 1; i <= N; i++) for (j = 1; j <= N; j++) T1[i][j] = 2*T1[i-1][j] + 3*T1[i][j-1];

	/* Algorithm B2: by anti-diagonals s = i + j = 2, 3, ..., 2N.
	 * The cells (i-1, j) and (i, j-1) both have i + j = s - 1, so they
	 * were filled in the previous pass over s. */
	for (s = 2; s <= 2*N; s++)
		for (i = 1; i <= N; i++) for (j = 1; j <= N; j++)
			if (i + j == s) T2[i][j] = 2*T2[i-1][j] + 3*T2[i][j-1];

	/* Compare every cell of both tables with the reference */
	for (i = 0; i <= N; i++) for (j = 0; j <= N; j++){
		if (T1[i][j] != R[i][j]) ok1 = 0;
		if (T2[i][j] != R[i][j]) ok2 = 0;
	}
	printf("T[%d][%d] = %lld\n", N, N, R[N][N]);     /* %lld prints a long long */
	/* Expected: both correct, option i) */
	printf("B1 correct: %s\nB2 correct: %s\n", ok1 ? "yes" : "no", ok2 ? "yes" : "no");
	return 0;
}
