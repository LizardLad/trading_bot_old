#include <stdio.h>
#include <stdlib.h>

#include "layers/activations.h"
#include "layers/matrix.h"
#include "layers/dense.h"
#include "layers/lstm.h"

//Need to set activation layers

float dense_1_weights_weights[] = {1.30000000000000004441, 1.30000000000000004441, 1.19999999999999995559, 1.19999999999999995559,};
struct matrix_f dense_1_weights = {.x=2, .y=2, .data=dense_1_weights_weights};
float dense_1_bias_weights[] = {-1.30000000000000004441, 0.00000000000000000000,};
struct matrix_f dense_1_bias = {.x=1, .y=2, .data=dense_1_bias_weights};
struct dense_layer dense_1 = {.weights=&dense_1_weights, .bias=&dense_1_bias, .output_x=1, .output_y=2, .input_x=2, .input_y=2, .activation=relu};
float dense_2_weights_weights[] = {-1.50000000000000000000, 0.80000000000000004441,};
struct matrix_f dense_2_weights = {.x=1, .y=2, .data=dense_2_weights_weights};
float dense_2_bias_weights[] = {0.00000000000000000000,};
struct matrix_f dense_2_bias = {.x=1, .y=1, .data=dense_2_bias_weights};
struct dense_layer dense_2 = {.weights=&dense_2_weights, .bias=&dense_2_bias, .output_x=1, .output_y=1, .input_x=1, .input_y=2, .activation=noop};

int main() {
	//Weights 
	//Right for 0,0
	//Right for 0,1
	//Right for 1,0
	//Right for 1,1
	float input_data[] = {1,1};
	struct matrix_f input = {.x=1, .y=2, .data=input_data};

	struct matrix_f result = {0};
	struct matrix_f result_2 = {0};
	result = Dense(dense_1, input);
	result_2 = Dense(dense_2, result);
	print_mat(result_2);
	free(result.data);
}