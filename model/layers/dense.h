#ifndef DENSE_H
#define DENSE_H

#include "matrix.h"

struct dense_layer {
	int input_x;
	int input_y;
	struct matrix_f *weights;
	struct matrix_f *bias;
	int output_x;
	int output_y;
	void (*activation)(struct matrix_f *);
};

struct matrix_f Dense(struct dense_layer layer, struct matrix_f input);

#endif