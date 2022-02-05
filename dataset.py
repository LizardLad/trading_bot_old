import os
import sys
import json 
import random
import logging
import functools
import multiprocessing
import tensorflow as tf
import tf_utils as utils

def valid_window_filter_internal(windows, full_timeseries=[], volatility_threshold=0.04):
	filtered_windows = []
	for window in windows:
		window_timeseries = full_timeseries[window['start_idx']:window['end_idx']]
		if(min(window_timeseries) != 0):
			volatility = (max(window_timeseries) - min(window_timeseries)) / min(window_timeseries)
			if(volatility >= volatility_threshold):
				filtered_windows.append(window)
	return filtered_windows

class CryptoDataset(tf.data.Dataset):
	def __new__(cls, samples_list, batch_size=2**11, feature_length=30*45, samples=8, stride_length=30*10, lookahead=30*60, gain_threshold=0.004, loss_threshold=0.0, training=True, class_balance=False, class_expansion=False, min_representation_percentage=0.5):
		windows_obj = {'prices': [], 'windows': []}

		logging.debug('Input sample length: {}'.format(len(samples_list)))
		logging.debug('Sample len: {}'.format(len(samples_list[0])))

		for price_list in samples_list:
			len_list = len(price_list) - lookahead - (feature_length * samples)
			left_over_samples = len_list % stride_length
			price_list = price_list[:-left_over_samples] if left_over_samples else price_list
			start_idx = len(windows_obj['prices'])
			end_idx = start_idx + feature_length * samples
			windows_obj['prices'].extend(price_list)
			generating_windows = True
			while((len(windows_obj['prices'][start_idx+stride_length+samples*feature_length:]) >= lookahead) and generating_windows == True):
				lookahead_value = windows_obj['prices'][end_idx + lookahead - 1]
				window = windows_obj['prices'][start_idx:end_idx]
				if(window[-1] == 0):
					generating_windows = False
					continue
				ratio = ((lookahead_value - window[-1]) / window[-1])
				if ratio > gain_threshold:
					label = 2
				elif ratio > loss_threshold and ratio <= gain_threshold:
					label = 1
				else:
					label = 0

				window_obj = {'start_idx': start_idx, 'end_idx': end_idx,
							  'label': label}
				windows_obj['windows'].append(window_obj)
				start_idx += stride_length
				end_idx += stride_length
		logging.debug('Unfiltered window count: {}'.format(len(windows_obj['windows'])))
		logging.debug('Real world time: {}m'.format(len(windows_obj)*15/len(samples_list)))
		windows_obj['windows'] = cls.__valid_window_filter(windows_obj['windows'], windows_obj['prices'])
		if(training):
			gain_list = []
			neutral_list = []
			loss_list = []
			logging.debug('Window count: {}'.format(len(windows_obj['windows'])))
			for window in windows_obj['windows']:
				if window['label'] == 2:
					gain_list.append(window)
				elif window['label'] == 1:
					neutral_list.append(window)
				else:
					loss_list.append(window)
		else:
			pass

		if(class_balance):
			if(class_expansion):
				unbalanced = True
				while unbalanced:
					longest_class_length = max([len(loss_list), len(gain_list), len(neutral_list)])
					balanced_length = min([len(loss_list), len(gain_list), len(neutral_list)])
					logging.debug('Unbalanced lengths:\n\t|_Gain: {}\n\t|_Neutral: {}\n\t|_Loss: {}'.format(len(gain_list), len(neutral_list), len(loss_list)))
					ratio = (balanced_length+2) / longest_class_length
					if(ratio <= min_representation_percentage):
						#Have to repeat stuff :/
						goal_length = int(min_representation_percentage * longest_class_length)
						list_to_expand = None
						list_name = ''
						if(len(neutral_list) == balanced_length):
							list_to_expand = neutral_list #Just a reference not a copy
							list_name = 'neutral'
						elif(len(gain_list) == balanced_length):
							list_to_expand = gain_list
							list_name = 'gain'
						else:
							list_to_expand = loss_list
							list_name = 'loss'
	
						list_long_enough = False
						list_to_expand_original = list_to_expand[:] #Do a copy
						while not list_long_enough:
							if(len(list_to_expand) >= goal_length):
								list_long_enough = True
							else:
								if(len(list_to_expand) * 2 <= goal_length):
									list_to_expand *= 2
								elif(len(list_to_expand) + len(list_to_expand_original) <= goal_length):
									list_to_expand.extend(list_to_expand_original)
								else:
									list_to_expand.extend(random.sample(list_to_expand_original, int(goal_length - len(list_to_expand))))
					else:
						unbalanced = False
			else:
				pass

			longest_class_length = max([len(loss_list), len(gain_list), len(neutral_list)])
			balanced_length = min([len(loss_list), len(gain_list), len(neutral_list)])
			logging.debug('Balanced lengths:\n\t|_Gain: {}\n\t|_Neutral: {}\n\t|_Loss: {}'.format(len(gain_list), len(neutral_list), len(loss_list)))
			loss_list = random.sample(loss_list, balanced_length-1)
			neutral_list = random.sample(neutral_list, balanced_length-1)
			gain_list = random.sample(gain_list, balanced_length-1)
		else:
			pass
		
		if(training):
			windows_obj['windows'] = gain_list
			windows_obj['windows'].extend(loss_list)
			windows_obj['windows'].extend(neutral_list)
		else:
			pass

		set_cardinality = len(windows_obj['windows'])
		batch_count = set_cardinality // batch_size
		logging.info('Batch count: {}'.format(batch_count))
		random.shuffle(windows_obj['windows'])
		window_start_indicies = [window_obj['start_idx'] for window_obj in windows_obj['windows']]
		window_end_indicies = [window_obj['end_idx'] for window_obj in windows_obj['windows']]
		window_labels = [window_obj['label'] for window_obj in windows_obj['windows']]
		window_prices = windows_obj['prices']

		return tf.data.Dataset.from_generator(
			cls._generator,
			output_signature = (tf.TensorSpec(shape=(batch_size, samples, feature_length), dtype=tf.float32), tf.TensorSpec(shape=(batch_size,), dtype=tf.int32)),
			args=(window_prices, window_start_indicies, window_end_indicies, window_labels, feature_length, samples, batch_size, batch_count, training)
		)
	
	def __valid_window_filter(windows, full_timeseries, volatility_threshold=0.001): #0.1% of movement in window
		pool=multiprocessing.Pool(8)
		part_func = functools.partial(valid_window_filter_internal, full_timeseries=full_timeseries, volatility_threshold=volatility_threshold)
		window_batches = []
		batch_size = 4
		for i, window in enumerate(windows):
			#Which batch are we on
			batch = i // batch_size
			if(i % batch_size == 0):
				window_batches.append([window])
			else:
				window_batches[batch].append(window)
			
		window_batches = pool.map(part_func, window_batches)
		windows = []
		for window_batch in window_batches:
			windows.extend(window_batch)

		return windows


	def _generator(window_prices, window_start_indicies, window_end_indicies, window_labels, feature_length, samples, batch_size, batch_count, training):
		for i in range(batch_count):
			features = []
			labels = []
			for j in range(batch_size):
				start_idx = window_start_indicies[i*batch_size + j]
				end_idx = window_end_indicies[i*batch_size + j]
				timeseries =  window_prices[start_idx:end_idx]
				timeseries = tf.convert_to_tensor(timeseries, dtype=tf.float32)
				timeseries = tf.reshape(timeseries, [samples, feature_length])
				label = window_labels[i*batch_size + j]
				labels.append(label)
				features.append(timeseries)
			labels = tf.convert_to_tensor(labels, dtype=tf.int32)
			features = tf.convert_to_tensor(features, dtype=tf.float32)
			if training: 
				yield (features, labels)
			else:
				yield (features, labels)

@tf.function
def gen_map(features, labels, feature_length=540, samples=8):
	map_func = functools.partial(inner_map, feature_length=feature_length, samples=samples)
	features = tf.vectorized_map(map_func, features)
	#Do a vectorized_map of ext_features ext_labels shouldn't change
	return (features, labels)

@tf.function
def inner_map(features, feature_length=540, samples=8):
	new_features = []
	for k in range(features.shape[0]):
		feature = tf.reshape(features[k], [feature_length*samples])
		angles = []
		for i in range(feature.shape[0] // feature_length):
			subwindow = feature[i*feature_length:(i+1)*feature_length]
			x = [j for j in range(subwindow.shape[0])]
			gradient = utils.linear_fit_get_gradient(x, subwindow)
			angles.append(utils.gradient_to_angle(gradient))
		timeseries_max = tf.math.reduce_max(tf.math.abs(feature))
		if(timeseries_max == 0.0):
			timeseries_max = tf.constant(1, dtype=tf.float32)
		scale_fac = tf.math.divide(tf.constant([1], dtype=tf.float32), timeseries_max)
		timeseries = tf.math.scalar_mul(tf.squeeze(scale_fac), feature)
		timeseries_min = tf.math.reduce_min(timeseries)
		timeseries = tf.math.subtract(timeseries, tf.squeeze(timeseries_min))
		for j, angle in enumerate(angles):
			angle = tf.convert_to_tensor([angle])
			partial_window = tf.slice(timeseries, begin=[j*feature_length], size=[feature_length-1])
			partial_window = tf.concat([partial_window, angle], 0)
			if(j == 0):
				new_timeseries = partial_window
			else:
				new_timeseries = tf.concat([new_timeseries, partial_window], 0)
		timeseries = new_timeseries
		timeseries = tf.reshape(timeseries, [samples, feature_length])
		new_features.append(timeseries)
	return tf.convert_to_tensor(new_features)
