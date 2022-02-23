import re
from nn_ops import matmul, matelemul, matadd, sigmoid, tanh

def lstm_4_split(s_t, hunit_start, hunit_end):
	#Problem make s_t[:][:hunit]
	output = [input[hunit_start:hunit_end] for input in s_t]
	return output

def LSTMCell(weight,x_t,h_tm1,c_tm1):
	kernel = weight[0]
	recurrent_kernel = weight[1]
	biases = [weight[2]]

	intermediate_1 = matmul(x_t, kernel)
	intermediate_2 = matmul(h_tm1, recurrent_kernel)
	intermediate_3 = matadd(intermediate_1, intermediate_2)
	#Element wise addition
	s_t = matadd(intermediate_3, biases)

	hunit = len(recurrent_kernel)
	i  = sigmoid(lstm_4_split(s_t, 0, hunit))
	f  = sigmoid(lstm_4_split(s_t, 1*hunit, 2*hunit))
	_c = tanh(lstm_4_split(s_t, 2*hunit, 3*hunit))
	o  = sigmoid(lstm_4_split(s_t, 3*hunit, 4*hunit))
	c_t = matadd(matelemul(i, _c), matelemul(f, c_tm1))
	#Element wise multiplication
	h_t = matelemul(o, tanh(c_t))
	
	return(h_t,c_t)

def LSTMLayer(weight, x, return_sequences=False):
	output = []
	h_t = [[0]*len(weight[1])]
	c_t = [[0]*len(weight[1])]
	for x_t in x:
		h_t, c_t = LSTMCell(weight, x_t, h_t, c_t)
		if(return_sequences):
			output.extend(h_t)
		else:
			output = h_t
	return output

inputs = [
	[[0.003]], 
	[[0.002]], 
	[[1]]
]
weights = [
	#Kernel
	[[-0.11138653755187988, 0.22896693646907806, -0.602969229221344, 0.4399285614490509, 0.4782624840736389, 0.03746636584401131, -0.44716590642929077, 0.10910264402627945, 0.41209378838539124, -0.10412748157978058, 0.13623058795928955, -0.7182826399803162]],
	#Recurrent Kernel
	[
		[-0.26069098711013794, -0.20290280878543854, 0.2166357934474945, -1.0301400423049927, -0.19240644574165344, 0.22681766748428345, -0.07238705456256866, -0.39520812034606934, -0.2155299335718155, -0.4451577961444855, -0.6217691898345947, 0.47965675592422485],
		[0.22313055396080017, 0.37778404355049133, -0.4554283618927002, 0.1716133952140808, 0.16404472291469574, 0.03692549839615822, 0.010164894163608551, 0.039925090968608856, 0.34017980098724365, 0.08782042562961578, 0.00042673543794080615, 0.35722169280052185],
		[0.12200673669576645, 0.3826979696750641, -0.6135170459747314, 0.44893917441368103, 0.14856140315532684, -0.5884832143783569, -0.023438910022377968, -0.3854145407676697, 0.23298323154449463, -0.23381271958351135, 0.29147616028785706, -0.6101807355880737]
	],
	#Bias
	[0.1017896980047226, 0.36655518412590027, 0.11918659508228302, 1.094984531402588, 1.2538317441940308, 1.1026681661605835, 0.13135625422000885, 0.08208376914262772, 0.1961633265018463, 0.380307674407959, 0.3846043050289154, 0.1758234202861786]
]

#Zero out state and hidden neurons first
print('Pure Python')
h_tm1 = [[0]*len(weights[1])]
c_tm1 = [[0]*len(weights[1])]
for input in inputs:
	h_tm1, c_tm1 = LSTMCell(weights, input, h_tm1, c_tm1)

print('h3 = {}'.format(h_tm1))
print('c3 = {}'.format(c_tm1))

print('LSTMLayer')
output = LSTMLayer(weights, inputs, return_sequences=True)
print('output = {}'.format(output))

#Print weights in C
fp = open('model.c', 'w')
layer_name = 'lstm_1'
fp.write('#include <stdio.h>\n')
fp.write('#include "matrix.h"\n')
fp.write('#include "lstm.h"\n')

def write_lstm_weights_as_c(fp, weights, layer_name):
	kernel = weights[0]
	recurrent_kernel = weights[1]
	bias = weights[2]
	kernel_str = ' '.join([f'{weight:.20f},' for weight in kernel[0]])
	recurrent_kernel_str = ' '.join([' '.join([f'{weight:.20f},' for weight in row]) for row in recurrent_kernel])
	bias_str = ' '.join([f'{weight:.20f},' for weight in bias])
	fp.write('float {}_kernel_weights[] = {}\n'.format(layer_name, '{' + kernel_str + '};' ))
	fp.write('struct matrix_f {layer_name}_kernel = '.format(layer_name=layer_name)+'{'+'.x={}, .y={}, .data={layer_name}_kernel_weights'.format(len(kernel), len(kernel[0]), layer_name=layer_name)+'};\n')
	fp.write('float {}_recurrent_kernel_weights[] = {}\n'.format(layer_name, '{' + recurrent_kernel_str + '};'))
	fp.write('struct matrix_f {layer_name}_recurrent_kernel = '.format(layer_name=layer_name)+'{'+'.x={}, .y={}, .data={layer_name}_recurrent_kernel_weights'.format(len(recurrent_kernel), len(recurrent_kernel[0]), layer_name=layer_name)+'};\n')
	fp.write('float {}_bias_weights[] = {}\n'.format(layer_name, '{' + bias_str + '};'))
	fp.write('struct matrix_f {layer_name}_bias = '.format(layer_name=layer_name)+'{'+'.x={}, .y={}, .data={layer_name}_bias_weights'.format(1, len(bias), layer_name=layer_name)+'};\n')

	#Input shapes
	input_x = 1
	input_y = len(kernel)
	#Sequence length is irrelevant

	return_sequences = True

	#Output shapes
	output_x = -1 if return_sequences else 1
	output_y = len(recurrent_kernel)
	#Sequence length is irrelevant
	
	return_sequences = 'true' if return_sequences else 'false'
	

	fp.write('struct lstm_layer {} = '.format(layer_name) + '{' + '.kernel=&{}, .recurrent_kernel=&{}, .bias=&{}, .input_x={}, .input_y={}, .output_x={}, .output_y={}, .return_sequences={}'.format(layer_name+'_kernel', layer_name+'_recurrent_kernel', layer_name+'_bias', input_x, input_y, output_x, output_y, return_sequences) + '};\n')
	fp.write('int main(){printf("%f", lstm_1_kernel_weights[0]); return 0;}')

write_lstm_weights_as_c(fp, weights, layer_name)
fp.close()