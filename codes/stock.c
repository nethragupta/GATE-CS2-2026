/*
   Method, with vectors (one entry per company A, B):
     shares s       = money invested / buying price   (entry by entry)
     price change d = new price - buying price
     profit         = s^T d   (shares x change in price, added up)        */
#include <stdio.h>
#include <stdlib.h>              
#include <math.h>                
#include "cprog/codes/msoft/libs/matfun.h"

int main(){
	int m = 2;                                  /* 2 companies: row 0 = A, row 1 = B */
	/* createMat(m, 1) makes an m x 1 column vector, stored as double ** */
	double **price  = createMat(m, 1);          /* buying price per share (Rs.) */
	double **invest = createMat(m, 1);          /* money put into each (Rs.)    */
	double **newp   = createMat(m, 1);          /* selling price per share (Rs.) */
	double **shares = createMat(m, 1);
	price[0][0]  = 50;  price[1][0]  = 80;
	invest[0][0] = 100; invest[1][0] = 80;
	newp[0][0]   = 55;  newp[1][0]   = 70;

	/* Number of shares bought in each company: 100/50 = 2 and 80/80 = 1 */
	for (int i = 0; i < m; i++) shares[i][0] = invest[i][0]/price[i][0];

	double **change = Matsub(newp, price, m, 1);   /* (55-50, 70-80) = (5, -10) */
	double sold   = Matdot(shares, newp, m);       /* 2 x 55 + 1 x 70 = 180     */
	double profit = Matdot(shares, change, m);     /* 2 x 5  + 1 x (-10) = 0    */

	printf("Shares (A, B):\n");
	printMat(shares, m, 1);                        /* prints the vector, one row per line */
	printf("Sold for Rs. %g, invested Rs. %g\n", sold, invest[0][0] + invest[1][0]);
	printf("Profit = Rs. %g\n", profit);           /* expected 0: option i) */

	/* Give back the memory createMat and Matsub took */
	freeMat(price, m); freeMat(invest, m); freeMat(newp, m);
	freeMat(shares, m); freeMat(change, m);
	return 0;
}
