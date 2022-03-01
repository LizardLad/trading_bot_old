#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "matrix.h"
#include "dense.h"

struct matrix_f Dense(struct dense_layer layer, struct matrix_f input) {
	struct matrix_f result = {0};
	struct matrix_f weight_transpose = transpose(*(layer.weights));
	matmul(input, weight_transpose, &result, false);
	free(weight_transpose.data);
	struct matrix_f after_bias = {0};
	matadd(*(layer.bias), result, &after_bias);
	free(result.data);
	//print_mat(after_bias);
	layer.activation(&after_bias);
	//print_mat(after_bias);
	return after_bias;
}