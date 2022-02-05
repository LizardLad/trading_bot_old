import os
import sys
import math
import logging
import tensorflow as tf

def tf_init():
	os.environ['TF_GPU_THREAD_MODE'] = 'gpu_private'
	gpus = tf.config.list_physical_devices('GPU')
	if(gpus):
		try:
			for gpu in gpus:
				tf.config.experimental.set_memory_growth(gpu, True)
			logical_gpus = tf.config.list_logical_devices('GPU')
			logging.debug('Physical GPUs: {} | Logical_GPUs: {}'.format(len(gpus), len(logical_gpus)))
		except RuntimeError as e:
			#No trading has occured yet
			#Safe exit
			logging.error('Experienced a RuntimeError in tf_init: '.format(e))
			sys.exit(3)
	else:
		pass
	return

@tf.function
def linear_fit(x, y):
	#Using y = mx + c
	#Y is the RHS in TF
	#X + 1*c is the Matrix input TF expects
	#Add the ones on the X matrix
	if(isinstance(x, list)):
		x = tf.constant(x)
	if(isinstance(y, list)):
		y = tf.constant(y)
	if(len(x.shape) == 1):
		x = tf.reshape(x, [x.shape[0], 1])
		ones = tf.cast(tf.ones(x.shape), tf.float32)
		x = tf.cast(x, tf.float32)
		x = tf.concat([x, ones], 1) #Concat ones on the 1st dimension
	if(len(y.shape) == 1):
		y = tf.reshape(y, [y.shape[0], 1])
	x = tf.cast(x, tf.float32)
	y = tf.cast(y, tf.float32)
	output = tf.linalg.lstsq(x, y, fast=False)
	return output

@tf.function
def linear_fit_get_gradient(x, y):
	return linear_fit(x,y)[0][0]

@tf.function
def gradient_to_angle(gradient):
	return tf.math.tan(gradient)

if __name__ == '__main__':
	x = [1, 2, 3, 4, 5]
	y = [4000, 4001, 4002, 4003, 4004]
	result = linear_fit(x, y)
	print(result)
	print(tf.convert_to_tensor(y).shape[0])
