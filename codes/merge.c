/*
   A merge of L (left half) and R (right half) is "void" when L followed by R
   is already sorted, i.e. the last element of L <= the first element of R.
   Method: run merge sort on the array and count those merges, then check
   the sorted result against cprog's quicksort. */
#include <stdio.h>
#include <stdlib.h>              
#include "cprog/codes/data/libs/datafun.h"

int voids = 0;                    /* global counter of void merges */

/* Merge the sorted halves a[lo..mid-1] (L) and a[mid..hi-1] (R) */
void merge(int a[], int lo, int mid, int hi){
	/* tmp holds the merged result; i walks through L, j through R,
	 * k is the next free place in tmp */
	int tmp[16], i = lo, j = mid, k = 0;
	if (a[mid-1] <= a[mid]){          /* L followed by R: void merge */
		voids++;
		printf("void merge: L ends %d, R starts %d\n", a[mid-1], a[mid]);
	}
	/* Repeatedly take the smaller front element of L and R.
	 * a[i++] uses a[i] and then moves i forward by one. */
	while (i < mid && j < hi) tmp[k++] = (a[i] <= a[j]) ? a[i++] : a[j++];
	while (i < mid) tmp[k++] = a[i++];     /* copy what is left of L */
	while (j < hi) tmp[k++] = a[j++];      /* copy what is left of R */
	for (k = 0; k < hi - lo; k++) a[lo + k] = tmp[k];   /* copy back into a */
}

/* Sort a[lo..hi-1] */
void msort(int a[], int lo, int hi){
	if (hi - lo < 2) return;          /* 0 or 1 element: already sorted */
	int mid = (lo + hi)/2;            /* split into two halves */
	msort(a, lo, mid);                /* sort the left half */
	msort(a, mid, hi);                /* sort the right half */
	merge(a, lo, mid, hi);            /* merge them */
}

int main(){
	int A[] = {10, 7, 8, 19, 41, 35, 25, 31};   /* the array from the question */
	int n = sizeof(A)/sizeof(A[0]);              /* number of elements: 8 */
	int B[8];
	for (int i = 0; i < n; i++) B[i] = A[i];     /* a copy for the quicksort check */

	msort(A, 0, n);
	printf("Sorted:     ");
	printData(A, n);                             /* prints the elements with spaces */
	printf("\nNumber of void merges = %d\n", voids);   /* expected 3 */

	/* Check: cprog's quicksort (arguments: first and last index) must agree */
	quicksort(B, 0, n - 1);
	printf("Quicksort:  ");
	printData(B, n);
	int same = 1;
	for (int i = 0; i < n; i++) if (A[i] != B[i]) same = 0;
	printf("\nMerge sort and quicksort agree: %s\n", same ? "yes" : "no");
	return 0;
}
