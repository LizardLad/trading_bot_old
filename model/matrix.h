#ifndef MATRIX_H
#define MATRIX_H

struct matrix_f {
	float *data;
	int x; //Number of rows
	int y; //Number of columns
};

int matmul(struct matrix_f a, struct matrix_f b, struct matrix_f *result);

#endif