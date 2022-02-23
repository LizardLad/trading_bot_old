#ifndef DENSE_H
#define DENSE_H

struct dense_layer {
	int input_x;
	int input_y;
	struct matrix_f *weights;
	struct matrix_f *bias;
	int output_x;
	int output_y;
};

#endif