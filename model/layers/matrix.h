#ifndef MATRIX_H
#define MATRIX_H

#include <stdbool.h>

struct matrix_f {
	float *data;
	int x; //Number of rows
	int y; //Number of columns
};

struct matrix_f transpose(struct matrix_f matrix);

int matmul(struct matrix_f a, struct matrix_f b, struct matrix_f *result, bool add);

int matadd(struct matrix_f a, struct matrix_f b, struct matrix_f *result);
int matelemul(struct matrix_f a, struct matrix_f *b);

struct matrix_f sigmoid(struct matrix_f a);
struct matrix_f tanh_mat(struct matrix_f a);

void print_mat(struct matrix_f a);

#endif