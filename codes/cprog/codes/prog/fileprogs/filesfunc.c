//Code by GVV Sharma
//April 14 2025
//using functions for all
#include <stdio.h>
#include <stdlib.h>

//Declaring functions 
void compare(int a,int b);
int sum(int a[], int m);
int *loadVec(char *str,int m);
int *createVec(int m);

//begin main function
int main() {
//Initializing sums
int a=0,b=0,m = 3;
//declare pointer arrays
int *a1,*b1;
	//Read  a from file a.dat
a1= loadVec("a.dat",m);
b1= loadVec("b.dat",m);
	//Read  b from file b.dat

//finding sum for A 
a = sum(a1,m);
//finding sum for B 
b = sum(b1,m);
//Call compare function 
compare(a,b);
 return 0;
}
//end main function

//compare function
void compare(int a,int b){
	 if (a>b){
	 printf("a scored more\n");
}
 else if (a<b){
	 printf("b scored more\n");
}
 else {
	 printf("they are equal\n");	 
}
 	}
//end compare function
//sum of vector elements
int sum(int *vec,int m){
int a=0;
  for (int i = 0; i < m; i++){
	  a=a+vec[i];
  }
  return a; //returning the sum to main
  }
//end sum function
//loading file data into vector
int *loadVec(char *str,int m){
FILE *fp;
int i;
int *vec=createVec(m);
	//Open file pointer
fp = fopen(str, "r");

//load data from file to array a1
 for(i=0;i<m;i++){
   fscanf(fp,"%d",&vec[i]);
  }
 
//Cose file pointer

fclose(fp);
return vec;
}

//end loading file data into vector
//Defining the function for vector creation
int *createVec(int m)
{
 int *vec;
 
 //Allocate memory to the pointer
vec = (int *)malloc(m * sizeof( vec));
 return vec;
}
