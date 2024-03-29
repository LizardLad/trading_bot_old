from nn_ops import noop, relu, matrix, matmul, matadd

def dense(weights, input, activation):
	#Input should be [[1, 2, 3, 4, 5, 6, ...]] 2D (1,None)
	#biases should be [1,2,3,4,5,...] 1D
	biases = weights[1]
	weights = weights[0]
	result = matmul(input, weights.transpose().tolist())
	result = matadd([biases], result)
	result = activation(result)
	return result

layers = []
#Layer 0
weights = matrix([
	[1.3, 1.3], #Neuron 0 weights
	[1.2, 1.2]  #Neuron 1 weights
], 2, 2)
biases = [-1.3, 0] #Neuron 0 and 1 biases respectively 
layers.append([weights, biases])
#Layer 1
weights = matrix(
[
	[-1.5, 0.8] #Neuron 0
], 1, 2)
biases = [0]
layers.append([weights, biases])

input = [[0,0]]
print(input)
output = input
for i, layer in enumerate(layers):
	if(i != len(layers) - 1):
		output = dense(layer, output, relu)
	else:
		output = dense(layer, output, noop)[0] #(1,None) to (None,) shape
print(output)

dense_1_weights = [[1.3, 1.3], [1.2, 1.2]]
dense_1_bias = [-1.3, 0]
dense_2_weights = [[-1.5, 0.8]]
dense_2_biases = [0]

layers = [[dense_1_weights, dense_1_bias], [dense_2_weights, dense_2_biases]]

fp = open('example_dense.c', 'w')
fp.write('#include <stdio.h>\n')
fp.write('#include "layers/matrix.h"\n')
fp.write('#include "layers/dense.h"\n')
fp.write('#include "layers/activations.h"\n\n')

def write_dense_weights_as_c(fp, layer_weights, layer_name, layer_activation):
	weights = layer_weights[0]
	bias = layer_weights[1]

	weights_str = ' '.join([' '.join([f'{weight:.20f},' for weight in row]) for row in weights])
	bias_str = ' '.join([f'{weight:.20f},' for weight in bias])
	fp.write('float {}_weights_weights[] = {};\n'.format(layer_name, '{' + weights_str + '}'))
	fp.write('struct matrix_f {}_weights = '.format(layer_name) + '{' + '.x={}, .y={}, .data={}_weights_weights'.format(len(weights), len(weights[0]), layer_name) + '};\n')
	fp.write('float {}_bias_weights[] = {}\n'.format(layer_name, '{' + bias_str + '};'))
	fp.write('struct matrix_f {}_bias = '.format(layer_name)+'{'+'.x={}, .y={}, .data={}_bias_weights'.format(1, len(bias), layer_name)+'};\n')

	#Input of a dense layer x = len(bias), y = len(weights[0])
	input_x = len(bias)
	input_y = len(weights[0])

	#Output of a dense layer x = 1, y = len(bias)
	output_x = 1
	output_y = len(bias)

	fp.write('struct dense_layer {} = '.format(layer_name) + '{' + '.weights=&{}_weights, .bias=&{}_bias, .output_x={}, .output_y={}, .input_x={}, .input_y={}, .activation={}'.format(layer_name, layer_name, output_x, output_y, input_x, input_y, activation) + '};\n')

#activation = layer.activation.__qualname__
activation = 'relu'
write_dense_weights_as_c(fp, layers[0], 'dense_1', activation)
activation = 'noop'
write_dense_weights_as_c(fp, layers[1], 'dense_2', activation)
fp.close()

fp.write('int main() {\n\tfloat input_data[] = {1,1};\n\tstruct matrix_f input = {.x=1, .y=2, .data=input_data};\n\
	\tstruct matrix_f result = {0};\n\
	\tstruct matrix_f result_2 = {0};\n\
	\tresult = Dense(dense_1, input);\n\
	\tresult_2 = Dense(dense_2, result);\n\
	\tprint_mat(result_2);\n\tfree(result.data);\n\tfree(result_2.data);\n\
	\treturn 0;\n}')