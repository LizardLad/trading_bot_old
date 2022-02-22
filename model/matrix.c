#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>
#include <cblas.h>

typedef enum {ROW, COLUM} MAJOR;

struct matrix_f {
	float *data;
	int x; //Number of rows
	int y; //Number of columns
	MAJOR major;
};

double diff_ms(struct timespec start, struct timespec end)
{
        struct timespec temp;
        if ((end.tv_nsec - start.tv_nsec) < 0) 
        {
                temp.tv_sec = end.tv_sec - start.tv_sec - 1;
                temp.tv_nsec = 1000000000 + end.tv_nsec - start.tv_nsec;
        } 
        else 
        {
                temp.tv_sec = end.tv_sec - start.tv_sec;
                temp.tv_nsec = end.tv_nsec - start.tv_nsec;
        }
		double ms = (temp.tv_sec * 1E9 + temp.tv_nsec) * 0.000001;
        return ms;
}

int matmul(struct matrix_f a, struct matrix_f b, struct matrix_f *result) {
	//Init result
	result->major=ROW;
	result->x=a.x;
	result->y=b.y;
	
	float *result_p = (float *)malloc(sizeof(float) * result->x * result->y);
	if(result_p == NULL) {return 1;}
	result->data = result_p;
	
	struct timespec start, end;
	clock_gettime(CLOCK_REALTIME, &start);
	cblas_sgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans, a.x, b.y, a.y, 1.0, a.data, a.y, b.data, b.y, 0.0, result->data, result->y);
	clock_gettime(CLOCK_REALTIME, &end);
	printf("Time taken: %lf ms\n", diff_ms(start, end));	

	return 0;
}

int main() {
	printf("%s\n",openblas_get_config());

	struct matrix_f a = {.x=100, .y=100, .major=ROW};
	a.data = (float *)malloc(a.x*a.y * sizeof(float));

	struct matrix_f b = {.x=100, .y=100, .major=ROW};
	b.data = (float *)malloc(b.x*b.y * sizeof(float));

	struct matrix_f c = {0};

	struct timeval start, end;
	gettimeofday(&start, NULL);
	matmul(a, b, &c);
	gettimeofday(&end, NULL);
	printf("Time taken: %lf ms\n", ((end.tv_sec * 1000000 + end.tv_usec) - (start.tv_sec * 1000000 + start.tv_usec))/1000.0);
	
	free(c.data);
	free(a.data);
	free(b.data);

	return 0;
}
