import json
import math

import numpy as np

def validate_matrix(a, dims=-1):
	nested = 0
	temp = a
	sizes = []
	while isinstance(temp, list):
		sizes.append(len(temp))
		temp = temp[0]
		nested += 1

	if(nested not in [2,3]):
		print(a)
		print(type(a))
		print(type(a[0]))
		raise ValueError('Invalid matrix dims. Expected 2 or 3, Received: {}'.format(nested))
	if(dims > 0 and nested != dims):
		print(a)
		print(type(a))
		print(type(a[0]))
		raise ValueError('Invalid matrix dims. Expected {}, Received: {}'.format(dims, nested))
	
	for idx_x in range(sizes[0]):
		if(nested == 3):
			for idx_y in range(sizes[1]):
				if(len(a[idx_x][idx_y]) != sizes[2]):
					return False
		if(len(a[idx_x]) != sizes[1]):
			return False
	return (True, nested, sizes)

#print(validate_matrix([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]))
#print(validate_matrix([[1,2],[3,4]]))
#print(validate_matrix([[[1, 2], [3, 4]], [[5, 6], [7, 8, 9]]]))
#print(validate_matrix([[1,2,5],[3,4]]))

def matmul(a, b):
	if(not (a_dims := validate_matrix(a, dims=2)) or not (b_dims := validate_matrix(b, dims=2))):
		raise ValueError('Invalid matrix')
	#Both matrices are valid
	a_dims = a_dims[2]
	b_dims = b_dims[2]

	n1, m1 = tuple(a_dims)
	n2, m2 = tuple(b_dims)
	if(m1 != n2):
		raise ValueError('Matrix sizes incompatible. A: {}, B: {}'.format(a_dims, b_dims))
	mat_dim = (n1, m2)
	c = []
	for i in range(n1):
		row = []
		for j in range(m2):
			sum = 0
			for k in range(m1):
				sum += a[i][k]*b[k][j]
			row.append(sum)
		c.append(row)
	#print('matmul output dims: {}'.format(mat_dim))
	return c

#a = [[1, 2, 3], [4, 5, 6]]
#b = [[10,11],[20,21],[30,31]]
#c = matmul(a, b)
#print(c)

def matadd(a, b):
	if(not (a_dims := validate_matrix(a, dims=2)) or not (b_dims := validate_matrix(b, dims=2))):
		raise ValueError('Invalid matrix')
	#Both matrices are valid
	a_dims = a_dims[2]
	b_dims = b_dims[2]

	n1, m1 = tuple(a_dims)
	n2, m2 = tuple(b_dims)
	if(n1 != n2 or m1 != m2):
		raise ValueError('Matrix sizes incompatible. A: {}, B: {}'.format(a_dims, b_dims))

	c = []
	for idx_x in range(n1):
		row = []
		for idx_y in range(m1):
			row.append(a[idx_x][idx_y] + b[idx_x][idx_y])
		c.append(row)

	return c

def matelemul(a, b):
	if(not (a_dims := validate_matrix(a, dims=2)) or not (b_dims := validate_matrix(b, dims=2))):
		raise ValueError('Invalid matrix')
	#Both matrices are valid
	a_dims = a_dims[2]
	b_dims = b_dims[2]

	n1, m1 = tuple(a_dims)
	n2, m2 = tuple(b_dims)
	if(n1 != n2 or m1 != m2):
		raise ValueError('Matrix sizes incompatible. A: {}, B: {}'.format(a_dims, b_dims))

	c = []
	for idx_x in range(n1):
		row = []
		for idx_y in range(m1):
			row.append(a[idx_x][idx_y] * b[idx_x][idx_y])
		c.append(row)
	return c

def exp(x):
	if(isinstance(x, list)):
		return list(map(lambda z: math.e**z, x))
	else:
		return math.e**x

def sigmoid(x):
	if(isinstance(x, list)):
		return list(map(lambda z: sigmoid(z), x))
	else:
		return 1.0/(1.0+exp(x))

def tanh(x):
	if(isinstance(x, list)):
		return list(map(lambda z: tanh(z), x))
	else:
		return math.tanh(x)

def lstm_4_split(s_t, hunit_start, hunit_end):
	#Problem make s_t[:][:hunit]
	output = [input[hunit_start:hunit_end] for input in s_t]
	return output

def LSTMlayer(weight,x_t,h_tm1,c_tm1):
	kernel = weight[0]
	recurrent_kernel = weight[1]
	biases = [weight[2]]

	#print(x_t)
	#print(h_tm1)
	#print(c_tm1)

	#Another matmul
	intermediate_1 = matmul(x_t, kernel)
	#Another matmul
	intermediate_2 = matmul(h_tm1, recurrent_kernel)
	#Element wise addition
	intermediate_3 = matadd(intermediate_1, intermediate_2)
	#Element wise addition
	s_t = matadd(intermediate_3, biases)
	hunit = len(recurrent_kernel)
	#print(f'hidden units: {hunit}')
	i  = sigmoid(lstm_4_split(s_t, 0, hunit))

	f  = sigmoid(lstm_4_split(s_t, 1*hunit, 2*hunit))

	_c = tanh(lstm_4_split(s_t, 2*hunit, 3*hunit))
	
	o  = sigmoid(lstm_4_split(s_t, 3*hunit, 4*hunit))
	
	c_t = matadd(matelemul(i, _c), matelemul(f, c_tm1))
	
	#Element wise multiplication
	h_t = matelemul(o, tanh(c_t))
	
	return(h_t,c_t)

def np_sigmoid(x):
    return(1.0/(1.0+np.exp(-x)))
def LSTMlayerNp(weight,x_t,h_tm1,c_tm1):
	#print(f'Input shapes: x: {x_t.shape}, h: {h_tm1.shape}, c: {c_tm1.shape}')
	kernel = np.array(weight[0])
	recurrent_kernel = np.array(weight[1])
	biases = np.array(weight[2])

	#Another matmul
	intermediate_1 = np.matmul(x_t, kernel)
	#Another matmul
	intermediate_2 = np.matmul(h_tm1, recurrent_kernel)
	#Element wise addition
	s_t = intermediate_1 + intermediate_2 + biases

	#print(f's_t shape: {s_t.shape}')
	hunit = recurrent_kernel.shape[0]
	#print(f'hidden units: {hunit}')
	i  = np_sigmoid(s_t[:,:hunit])
	#print(f'i shape: {i.shape}')
	f  = np_sigmoid(s_t[:,1*hunit:2*hunit])
	#print(f'f shape: {f.shape}')
	_c = np.tanh(s_t[:,2*hunit:3*hunit])
	#print(f'_c shape: {_c.shape}')
	o  = np_sigmoid(s_t[:,3*hunit:])
	#print(f'o shape: {o.shape}')
	c_t = i*_c + f*c_tm1
	#print(f'c_t shape: {c_t.shape}')
	h_t = o*np.tanh(c_t)
	#print(f'h_t shape: {h_t.shape}')
	return(h_t,c_t)

inputs = [0.003, 0.002, 1]
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
c_tm1 = np.array([0]*3).reshape(1,3).tolist()
h_tm1 = np.array([0]*3).reshape(1,3).tolist()
for input in inputs:
	h_tm1, c_tm1 = LSTMlayer(weights, [[input]], h_tm1, c_tm1)

print('h3 = {}'.format(h_tm1))
print('c3 = {}'.format(c_tm1))

print('Numpy')
c_tm1 = np.array([0]*3).reshape(1,3).tolist()
h_tm1 = np.array([0]*3).reshape(1,3).tolist()
for input in inputs:
	h_tm1, c_tm1 = LSTMlayerNp(weights, np.array([[input]]), np.array(h_tm1), np.array(c_tm1))

print('h3 = {}'.format(h_tm1))
print('c3 = {}'.format(c_tm1))