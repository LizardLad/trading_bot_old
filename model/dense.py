from nn_ops import noop, relu, matrix, matmul, matadd

def dense(weights, input, activation):
	#Input should be [[1, 2, 3, 4, 5, 6, ...]] 2D (1,None)
	#biases should be [1,2,3,4,5,...] 1D
	biases = weights[1]
	weights = weights[0]
	result = matmul(input, weights.transpose().tolist())
	return matadd([biases], result)

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
output = input
for i, layer in enumerate(layers):
	if(i != len(layers) - 1):
		output = dense(layer, output, relu)
	else:
		output = dense(layer, output, noop)[0] #(1,None) to (None,) shape
print(output)