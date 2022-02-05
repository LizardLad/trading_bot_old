import os
import tensorflow as tf
import numpy as np
from dataset import CryptoDataset
from model import LSTMModel

def inference(model, windows, samples, feature_length)
	batch_size = 2**6 #Applies only if doing multiple inferences at once
	confidence = 95 #%
	neutral_idx = 1

	input_dim = (batch_size, samples, feature_length)
	inference_dataset = CryptoDataset(windows, batch_size=batch_size, 
					feature_length=feature_length, samples=samples, training=False)
	inference_dataset.prefetch(tf.data.AUTOTUNE).cache()

	pred = model.predict(inference_dataset)
	print('Inference done!')
	return pred

#Confidence matrix generation	
#Useful in the future for model diagnostics
	#y_pred = []
	#y_true = []
	#x = []
	#for features, labels in test_dataset:
	#	y_true.extend(labels)
#		pred = model.predict(features, batch_size=batch_size)
#		predicted_class_indicies = np.argmax(pred, axis=-1)
#		for idx, prediction in enumerate(pred):
#			if prediction[predicted_class_indicies[idx]] <= confidence / 100:
#				predicted_class_idx = neutral_idx
#			else:
#				predicted_class_idx = predicted_class_indicies[idx]
#			y_pred.append(predicted_class_idx)
#
#	losses = [label for label in y_true if label == 0]
#	neutrals = [label for label in y_true if label == 1]
#	gains = [label for label in y_true if label == 2]
#	print('Class distribution: loss: {} | neutral: {} | gain: {}'.format(len(losses), len(neutrals), len(gains)))
#
#	y_true = tf.convert_to_tensor(y_true, dtype=tf.float32)
#	confusion_matrix = tf.math.confusion_matrix(y_true, y_pred)
#	print(confusion_matrix)
