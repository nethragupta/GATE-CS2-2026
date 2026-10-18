//code by GVV Sharma
//April 22, 2025
//function to compute the nth power of an integer

#include <stdio.h>

//function to compute a to the power n
int power(int a,int n){
	 if (n == 0){
	 return(1);
	 }
	 else{
		 return a*power(a,n-1);
	 }
 	}
//end function to compute a to the power n

//begin main function
int main(void) {
 int a=9,n=3;
 
 //call the function to compute 9 to the power 3 
printf("%d\n",power(9,3));
 
 return 0;
}
//end main function



