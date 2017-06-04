#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

double get_time()
{
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return tv.tv_sec + tv.tv_usec * 1e-6;
}

double multiply(int n)
{
  double* a = (double*)malloc(n * n * sizeof(double)); // Matrix A
  double* b = (double*)malloc(n * n * sizeof(double)); // Matrix B
  double* c = (double*)malloc(n * n * sizeof(double)); // Matrix C

  // Initialize the matrices to some values.
  int i, j;
  for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++) {
      a[i * n + j] = i * n + j; // A[i][j]
      b[i * n + j] = j * n + i; // B[i][j]
      c[i * n + j] = 0; // C[i][j]
    }
  }

  double begin = get_time();


  /**************************************/
  /* Write code to calculate C = A * B. */
  /**************************************/
  double sum;
  int k;
  for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++) {
      sum=0;
      for(k=0;k<n;k++){
	
        sum += a[i*n+k]*b[k*n+j]; // C[i][j]
      }
      c[i*n+j]=sum;
    }
  }
  double end = get_time();
  double timeuse;
  timeuse=end-begin;
  printf("time: %.6lf sec\n", timeuse);
  //

  // Print C for debugging. Comment out the print before measuring the execution time.
  sum=0;
  for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++) {
      sum += c[i * n + j];
      // printf("c[%d][%d]=%lf\n", i, j, c[i * n + j]);
    }
  }
  // Print out the sum of all values in C.
  // This should be 450 for N=3, 3680 for N=4, and 18250 for N=5.
  printf("sum: %.6lf\n", sum);

  free(a);
  free(b);
  free(c);
  return timeuse;  //return time to print to file in main()
}

int main(int argc, char** argv)
{
  if (argc != 2) {
    printf("usage: %s N\n", argv[0]);
    return -1;
  }
  FILE *f;
  f=fopen("multiplymatrix.dat","w");
  int n = atoi(argv[1]);
  int i;
  int di;
  di=n/10;
  for(i=0;i<=n;i+=di){
    fprintf(f,"%d\t%.6lf\n",i,multiply(i));
  }
  fclose(f);
  return 0;
}
