#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <cblas-openblas.h>

typedef enum {COLUMN, ROW} MAJOR;

//float
struct matrix_f {
	float *data;
	float *data_aligned;
	int x; //Number of rows
	int y; //Number of columns
	MAJOR major;
};

//Transpose matricies
struct matrix_f mat_f_transpose(struct matrix_f matrix) {
    float *temp = (float *) malloc(sizeof(float) * matrix.x * matrix.y);
    for (int i = 0; i < matrix.x; i++) {      // i is row index
        for (int j = 0; j < matrix.y; j++) {  // j is column index
            temp[j * matrix.x + i] = matrix.data[i * matrix.y + j];
        }
    }
    memcpy(matrix.data, temp, sizeof(float) * matrix.x * matrix.y);
    free(temp);
	int temp_x = matrix.x;
	matrix.x = matrix.y;
	matrix.y = temp_x;

	if(matrix.major == ROW){matrix.major = COLUMN;}
	else {matrix.major = ROW;}
    return matrix;
}

struct matrix_f convert_to_row_major(struct matrix_f matrix) {
	if(matrix.major == ROW) {return matrix;}
	float *temp = (float *) malloc(sizeof(float) * matrix.x * matrix.y);
    for (int i = 0; i < matrix.x; i++) {      // i is row index
        for (int j = 0; j < matrix.y; j++) {  // j is column index
            temp[j * matrix.x + i] = matrix.data[i * matrix.y + j];
        }
    }
    memcpy(matrix.data, temp, sizeof(float) * matrix.x * matrix.y);
    free(temp);

	matrix.major = ROW;
    return matrix;
}

void print_mat(struct matrix_f a) {
	for(int i = 0; i < a.x; i++) {
		for(int j = 0; j < a.y; j++) {
			printf("%f  ", a.data[i*a.y+j]);
		}
		printf("\n");
	}
}

struct matrix_f convert_to_column_major(struct matrix_f matrix) {
    if (matrix.major == COLUMN) {
        return matrix;
    }

    float *temp = (float *) malloc(sizeof(float) * matrix.x * matrix.y);

    for (int i = 0; i < matrix.x; i++) {      // i is row index
        for (int j = 0; j < matrix.y; j++) {  // j is column index
            temp[j * matrix.x + i] = matrix.data[i * matrix.y + j];
        }
    }

    memcpy(matrix.data, temp, sizeof(float) * matrix.x * matrix.y);
    free(temp);
    matrix.major = COLUMN;

    return matrix;
}

//Dynamically allocate result matrix and calculate
int matmul(struct matrix_f a, struct matrix_f b, struct matrix_f *result) {
	//Init result
	result->major=ROW;
	result->x=a.x;
	result->y=b.y;
	
	float *result_p = (float *)malloc(sizeof(float) * result->x * result->y);
	if(result_p == NULL) {return 1;}
	result->data = result_p;

	if(a.major != ROW) {a = convert_to_row_major(a);}
	if(b.major != COLUMN) {b = convert_to_column_major(b);}
	clock_t start, end;
	double cpu_time_used;
	start=clock();
	//for(int i = 0; i < 10000; i++) {
		//b = convert_to_column_major(b);
	//}
	end=clock();
	cpu_time_used = ((double)(end-start)) / CLOCKS_PER_SEC;
	printf("Execution time transpose %lf\n", cpu_time_used);

	//Right majors to to the calculation
	start = clock();
	for(int i = 0; i < a.x; i++) {
		int i_offset = i * a.y;
		for(int j = 0; j < b.y; j++) {
			float sum = 0;
			int j_offset = j * b.x;
			for(int k = 0; k < b.x; k++) {
				sum += a.data[i_offset+k]*b.data[j_offset + k];
			}
			result->data[i*a.x+j] = sum;
		}
	}
	end = clock();
	cpu_time_used = ((double)(end-start)) / CLOCKS_PER_SEC;
	printf("Execution time mul %lf\n", cpu_time_used);

	return 0;
}

int main() {
	//Own implementation

	//struct matrix_f a = {.x=1, .y=3, .major=ROW};
	//struct matrix_f a = {.x=2, .y=3, .major=ROW};
	struct matrix_f a = {.x=1000, .y=1000, .major=ROW};
	a.data = (float *)calloc(a.x*a.y, sizeof(float));

	//float a_data[] = {1, 2, 3}; //[[1, 2, 3], [4, 5, 6]]
	//float a_data[] = {1, 2, 3, 4, 5, 6}; //[[1, 2, 3], [4, 5, 6]]
	//memcpy(a.data, a_data, sizeof(float)*6);
	
	//struct matrix_f b = {.x=3, .y=2, .major=ROW};
	struct matrix_f b = {.x=1000, .y=1000, .major=ROW};
	b.data = (float *)calloc(b.x*b.y, sizeof(float));
	//float b_data[] = {10,11,20,21,30,31}; //[[10,11],[20,21],[30,31]]
	//memcpy(b.data, b_data, sizeof(float)*6);

	struct matrix_f c = {0};


	clock_t start, end;
	double cpu_time_used;
	start=clock();
	//for(int i = 0; i < 10000; i++) {
		matmul(a, b, &c);
	//}
	end=clock();
	cpu_time_used = ((double)(end-start)) / CLOCKS_PER_SEC;
	printf("Execution time %lf\n", cpu_time_used);
	
	//printf("Print result matrix\n");
	//print_mat(result);
	//free(c.data);
	//free(a.data);
	//free(b.data);



	//OpenBLAS
	start=clock();
	cblas_sgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans, a.x, b.y, a.y, 1.0, a.data, a.y, b.data, b.y, 1.0, c.data, c.y);
	end=clock();
	cpu_time_used = ((double)(end-start)) / CLOCKS_PER_SEC;
	printf("Execution time %lf\n", cpu_time_used);








	free(c.data);
	free(a.data);
	free(b.data);

	return 0;
}