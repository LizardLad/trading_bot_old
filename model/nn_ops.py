import math

###
# Activations
###

def relu(x):
	if(isinstance(x, list)):
		return list(map(lambda z: relu(z), x))
	else:
		return max([0, x])

def noop(x):
	return x

def exp(x):
	if(isinstance(x, list)):
		return list(map(lambda z: math.e**z, x))
	else:
		return math.e**x

def sigmoid(x):
	if(isinstance(x, list)):
		return list(map(lambda z: sigmoid(z), x))
	else:
		return 1.0/(1.0+exp(-x))

def tanh(x):
	if(isinstance(x, list)):
		return list(map(lambda z: tanh(z), x))
	else:
		return math.tanh(x)

###
# Matrix math
###

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

if __name__ == '__main__':
	print(validate_matrix([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]))
	print(validate_matrix([[1,2],[3,4]]))
	print(validate_matrix([[[1, 2], [3, 4]], [[5, 6], [7, 8, 9]]]))
	print(validate_matrix([[1,2,5],[3,4]]))

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

if __name__ == '__main__':
	a = [[1, 2, 3], [4, 5, 6]]
	b = [[10,11],[20,21],[30,31]]
	c = matmul(a, b)
	print(c)

	a = [[1,2,3]]
	b = [[10, 11], [20, 21], [30, 31]]
	c = matmul(a,b)
	print(c)

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

###
# C style matrix implementation
###

class matrix():
	def __init__(self, data, x, y):
		output = []
		if(isinstance(data[0], list)):
			for segment in data:
				output.extend(segment)
			data = output
		assert(not isinstance(data[0], list))
		assert(len(data) == x*y)
		self.data = data
		self.x = x
		self.y = y
	def transpose(self):
		#Stored row major
		new_data = []
		for row_idx in range(self.y):
			for column_idx in range(self.x):
				new_data.append(self.data[column_idx*self.y+row_idx])
		data = new_data
		return matrix(data, self.y, self.x)
	def tolist(self):
		output = []
		for i in range(self.x):
			row = []
			for j in range(self.y):
				row.append(self.data[i*self.y + j])
			output.append(row)
		return output
	