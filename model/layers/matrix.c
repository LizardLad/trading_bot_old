#include <sys/time.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <time.h>
#include <cblas.h>

#include "matrix.h";

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

int matmul(struct matrix_f a, struct matrix_f b, struct matrix_f *result, bool add) {
	if(!add) { //If we are adding then result already has populated data
		result->x=a.x;
		result->y=b.y;
		float *result_p = (float *)malloc(sizeof(float) * result->x * result->y);
		if(result_p == NULL) {return 1;}
		result->data = result_p;
	}
	
	struct timespec start, end;
	clock_gettime(CLOCK_REALTIME, &start);
	if(!add) {
		cblas_sgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans, a.x, b.y, a.y, 1.0, a.data, a.y, b.data, b.y, 0.0, result->data, result->y);
	} else {
		cblas_sgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans, a.x, b.y, a.y, 1.0, a.data, a.y, b.data, b.y, 1.0, result->data, result->y);
	}
	clock_gettime(CLOCK_REALTIME, &end);
	printf("Time taken: %lf ms\n", diff_ms(start, end));	

	return 0;
}

/*int main() {
	struct matrix_f a = {.x=1000, .y=1000};
	a.data = (float *)malloc(a.x*a.y * sizeof(float));
	for(int i = 0; i < a.x*a.y+1; i++) {
		a.data[i] = (float) i;
	}

	struct matrix_f b = {.x=1000, .y=1000};
	b.data = (float *)malloc(b.x*b.y * sizeof(float));
	for(int i = 0; i < b.x*b.y+1; i++) {
		b.data[i] = (float) i;
	}

	struct matrix_f c = {0};

	matmul(a, b, &c);

	free(c.data);
	free(a.data);
	free(b.data);

	return 0;
}*/


struct matrix_f transpose(struct matrix_f matrix) {
	struct matrix_f result = {0};
    float *temp = (float *) malloc(sizeof(float) * matrix.x * matrix.y);
	if(temp == NULL) {return result;}
	result.data = temp;

    for (int i = 0; i < matrix.x; i++) {      // i is row index
        for (int j = 0; j < matrix.y; j++) {  // j is column index
            result.data[j * matrix.x + i] = matrix.data[i * matrix.y + j];
        }
    }
	result.y = matrix.x;
	result.x = matrix.y;

    return result;
}