#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "matrix.h"
#include "dense.h"

struct matrix_f Dense(struct dense_layer layer, struct matrix_f input, struct matrix_f activation(struct matrix_f)) {
	struct matrix_f result = {0};
	struct matrix_f weight_transpose = transpose(*(layer.weights));
	matmul(input, weight_transpose, &result, false);
	free(weight_transpose.data);
	struct matrix_f after_bias = {0};
	matadd(*(layer.bias), result, &after_bias);
	free(result.data);
	result = activation(after_bias);

	return result;
}