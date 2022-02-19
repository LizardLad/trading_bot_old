def relu(x):
	return max([0, x])

def clear(x):
	return x

def dense(weights_list, biases, input, activation):
	#Input should be [1, 2, 3, 4, 5, 6, ...] 1D
	outputs = []
	for i, bias in enumerate(biases):
		sum = 0
		for j, weight in enumerate(weights_list[i]):
			sum += weight * input[j]
		neuron = sum + bias
		neuron = activation(neuron)
		outputs.append(neuron)
	return outputs

layers = []
#Layer 0
weights = \
[
	[1.3, 1.3], #Neuron 0 weights
	[1.2, 1.2]  #Neuron 1 weights
]
biases = [-1.3, 0] #Neuron 0 and 1 biases respectively 
layers.append([weights, biases])
#Layer 1
weights = \
[
	[-1.5, 0.8] #Neuron 0
]
biases = [0]
layers.append([weights, biases])

input = [1, 0]
for i, layer in enumerate(layers):
	weights = layer[0]
	biases = layer[1]
	if(i != len(layers) - 1):
		input = dense(weights, biases, input, relu)
	else:
		output = dense(weights, biases, input, clear)
print(output)