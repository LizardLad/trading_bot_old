import os
import sys
import math
import time
import config
import logging
import functools
import numpy as np
import tensorflow as tf
from model import LSTMModel
from tf_utils import tf_init
from interface import FileReader
from dataset import CryptoDataset, gen_map

from asset import assets

def train_main(args):
	#This trains from files
	#Read from files
	tf_init()
	if(args.dir and args.input):
		logging.error('Input file and input dir set. Only one at a time is supported!')
		sys.exit(1)
	elif(args.dir):
		files = os.listdir(args.dir)
		files = [os.path.join(args.dir, filename) for filename in files]
		if(len(files) == 0):
			logging.error('No files in input directory')
			sys.exit(1)
	elif(args.input):
		#Make sure file exists
		if(not os.path.isfile(args.input)):
			logging.error('Argument provided to input is not a file')
			sys.exit(1)
		else:
			pass
		files = [args.input]
	else:
		logging.error('Training mode provided without input to train on')
		sys.exit(1)

	desired_train_split = float(config.cfg.get('train_split', 0.7))
	batch_size = int(config.cfg.get('batch_size', 2**6))
	quote_time_delta = int(config.cfg.get('quote_time_delta', 5))
	samples_per_minute = int(math.floor(60/quote_time_delta))
	feature_length = int(config.cfg.get('feature_length_minutes', 75)) * samples_per_minute
	samples = int(config.cfg.get('samples', 8))
	stride_length = int(config.cfg.get('stride_length_minutes', 2)) * samples_per_minute
	lookahead = int(config.cfg.get('lookahead_minutes', 45)) * samples_per_minute
	gain_threshold = float(config.cfg.get('gain_threshold', 2.5)) / 100.0 #Make %
	loss_threshold = float(config.cfg.get('loss_threshold', 0.0)) / 100.0 #Make %
	max_epochs = int(config.cfg.get('epochs', 6))
	lr = float(config.cfg.get('learning_rate', 1e-3))
	lr_decay = float(config.cfg.get('learning_rate_decay', 1e-6))
	class_count = int(config.cfg.get('class_count', 3))
	model_filepath = str(config.cfg.get('model_filepath', './model'))
	min_rep_percent = float(config.cfg.get('min_class_representation_percentage', 0.5))
	
	if(args.new_model):
		logging.info('Creating new model')
		model = create_model(class_count, samples, feature_length)
	else:
		logging.info('Loading existing model: {}'.format(model_filepath))
		model = tf.keras.models.load_model(model_filepath)
	model_interface = CryptoModel(model)
	
	file_reader = FileReader(os.environ.get('LIBCRYPTO_PATH', 'libcrypto/libcrypto.so'))
	for idx, filepath in enumerate(files):
		if(idx): #If it isn't the first file then clear some memory
			tf.keras.backend.clear_session()
			if(args.output):
				model = tf.keras.models.load_model(args.output)
			else:
				model = tf.keras.models.load_model(model_filepath)
			model_interface = CryptoModel(model)
		else:
			pass

		logging.debug('Starting to read file: {}'.format(filepath))
		start_time = time.time()
		file_reader.read_from_file(filepath)
		logging.debug('Reading file took {}s'.format(time.time() - start_time))
		start_time = time.time()
		for asset in assets.values():
			ask_price_samples = file_reader.get_samples_by_asset_id(asset.asset_id, filtered=True, side='ask')
			mid_price_samples = file_reader.get_samples_by_asset_id(asset.asset_id, filtered=True, side='mid')
			bid_price_samples = file_reader.get_samples_by_asset_id(asset.asset_id, filtered=True, side='bid')
			timestamps = file_reader.get_timestamps_by_asset_id(asset.asset_id, filtered=True)
			asset.add_samples_from_file(ask_price_samples, mid_price_samples, bid_price_samples, timestamps, filtered=True)
		logging.debug('Data filtering took: {}s'.format(time.time()-start_time))
		file_reader.free()
		logging.debug('File time span: {}s'.format(timestamps[-1] - timestamps[1]))
		
		model= tf.keras.models.load_model(model_filepath)
		model_interface = CryptoModel(model)
		
		price_samples = []
		for asset in assets.values():
			ask_price_samples = asset.get_samples(filtered=True, side='ask')
			if(len(ask_price_samples) > 0):
				price_samples.extend(ask_price_samples)

		model_interface.train_eval_init(batch_size, feature_length, samples, stride_length, lookahead, gain_threshold, loss_threshold, training=True)
		model_interface.train(price_samples, desired_train_split, lr, lr_decay, max_epochs, min_rep_percent=min_rep_percent, class_expansion=False)

		if(args.output):
			model_interface.model.save(args.output)
		else:
			model_interface.model.save(model_filepath)

	logging.info('Training complete')
	return 0

def eval_main(args):
	tf_init()
	if(args.dir and args.input):
		logging.error('Input file and input dir set. Only one at a time is supported!')
		sys.exit(1)
	elif(args.dir):
		files = os.listdir(args.dir)
		files = [os.path.join(args.dir, filename) for filename in files]
		if(len(files) == 0):
			logging.error('No files in input directory')
			sys.exit(1)
		else:
			pass
	elif(args.input):
		#Make sure file exists
		if(not os.path.isfile(args.input)):
			logging.error('Argument provided to input is not a file')
			sys.exit(1)
		else:
			pass
		files = [args.input]
	else:
		logging.error('Evaluation mode provided without input to evalutate with')
		sys.exit(1)

	batch_size = int(config.cfg.get('batch_size', 2**6))
	quote_time_delta = int(config.cfg.get('quote_time_delta', 5))
	samples_per_minute = int(math.floor(60/quote_time_delta))
	feature_length = int(config.cfg.get('feature_length_minutes', 75)) * samples_per_minute
	samples = int(config.cfg.get('samples', 8))
	stride_length = int(config.cfg.get('stride_length_minutes', 2)) * samples_per_minute
	lookahead = int(config.cfg.get('lookahead_minutes', 45)) * samples_per_minute
	gain_threshold = float(config.cfg.get('gain_threshold', 2.5)) / 100 #In %
	loss_threshold = float(config.cfg.get('loss_threshold', 0.0)) / 100#In %
	model_filepath = str(config.cfg.get('model_filepath', './model'))

	file_reader = FileReader(os.environ.get('LIBCRYPTO_PATH', 'libcrypto/libcrypto.so'))

	y_true = []
	y_pred = []
	for filepath in enumerate(files):
		#Read one files contents into asset instances
		logging.info('Evaluating model with file: {}'.format(filepath))
		file_reader.read_from_file(filepath)
		for asset in assets.values(): #TODO only grab assets that have information in the files
			ask_price_samples = file_reader.get_samples_by_asset_id(asset.asset_id, filtered=True, side='ask')
			mid_price_samples = file_reader.get_samples_by_asset_id(asset.asset_id, filtered=True, side='mid')
			bid_price_samples = file_reader.get_samples_by_asset_id(asset.asset_id, filtered=True, side='bid')
			timestamps = file_reader.get_timestamps_by_asset_id(asset.asset_id, filtered=True)
			if(not (len(ask_price_samples) == 0 or len(mid_price_samples) == 0 or len(bid_price_samples) == 0 or len(timestamps) == 0)): #Must have something in them
				asset.add_samples_from_file(ask_price_samples, mid_price_samples, bid_price_samples, timestamps, filtered=True)

		file_reader.free()
		logging.debug('File time span: {}s'.format(timestamps[-1] - timestamps[1]))
		
		model= tf.keras.models.load_model(model_filepath)
		model_interface = CryptoModel(model)
		
		price_samples = []
		for asset in assets.values():
			ask_price_samples = asset.get_samples(filtered=True, side='ask')
			if(len(ask_price_samples) > 0):
				price_samples.extend(ask_price_samples)
		
		model_interface.train_eval_init(batch_size, feature_length, samples, stride_length, lookahead, gain_threshold, loss_threshold, training=False)
		true_y, pred_y = model_interface.eval(price_samples)
		y_true.extend(true_y)
		y_pred.extend(pred_y)
	for confidence in range(50, 100, 2):
		model_interface.confidence_matrix(confidence=confidence/100.0, y_pred=y_pred, y_true=y_true)
	return 0

class CryptoModel():
	def __init__(self, model):
		self.model = model

	def lr_schedule(self, epoch, lr):
		if epoch < 2:
			return lr
		else:
			return lr * tf.math.exp(-0.3)

	def train_eval_init(self, batch_size, feature_length, samples, stride_length, lookahead, gain_threshold, loss_threshold, checkpoint_path='./checkpoints', training=True, logs='./logs/'):
		self.batch_size = batch_size
		self.feature_length = feature_length
		self.samples = samples
		self.stride_length = stride_length
		self.lookahead = lookahead
		self.gain_threshold = gain_threshold
		self.loss_threshold = loss_threshold
		
		if(training):
			self.checkpoint_path = checkpoint_path
			self.callbacks = [#tf.keras.callbacks.ModelCheckpoint(filepath=self.checkpoint_path+'acc_optim', 
								#save_best_only=True, monitor='val_sparse_categorical_accuracy', verbose=1), 
						#tf.keras.callbacks.LearningRateScheduler(self.lr_schedule),
						tf.keras.callbacks.ModelCheckpoint(filepath=self.checkpoint_path+'loss_optim', 
								save_best_only=True, monitor='val_loss',verbose=1), 
						tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3),
						tf.keras.callbacks.TensorBoard(log_dir=logs, histogram_freq=1)]
		else:
			self.y_true = []
			self.y_pred = []

	def train(self, price_samples, desired_train_split, lr, lr_decay, epochs, class_expansion=False, min_rep_percent=0.05):
		train_samples = []
		val_samples = []

		min_len = (self.feature_length * self.samples) + (self.stride_length * 2) + self.lookahead
		for sample in price_samples:
			train_len = math.floor(len(sample) * desired_train_split)
			if(len(sample) - train_len < min_len and len(sample) >= min_len * 2):
				logging.debug('Had to change the ratio. Val length now: {}'.format(min_len))
				train_samples.append(sample[min_len:])
				val_samples.append(sample[:min_len])
			elif(len(sample) < min_len * 2):
				logging.warning('Sample not long enough for train/val split')
				pass
			else:
				train_samples.append(sample[:train_len])
				val_samples.append(sample[train_len:])

		logging.debug('Length train samples: {}'.format(len(train_samples)))
		logging.debug('Length val samples: {}'.format(len(val_samples)))
		if(len(val_samples) == 0 or len(train_samples) == 0):
			logging.warning('Either val samples or train samples has no samples')
			return
		else:
			pass

		train_dataset = CryptoDataset(train_samples, batch_size=self.batch_size, 
			feature_length=self.feature_length, samples=self.samples, 
			stride_length=self.stride_length, lookahead=self.lookahead, 
			gain_threshold=self.gain_threshold, loss_threshold=self.loss_threshold,
			class_balance=True, min_representation_percentage=min_rep_percent, 
			class_expansion=class_expansion)
		val_dataset = CryptoDataset(val_samples, batch_size=self.batch_size, 
			feature_length=self.feature_length, samples=self.samples, 
			stride_length=self.stride_length, lookahead=self.lookahead, 
			gain_threshold=self.gain_threshold, loss_threshold=self.loss_threshold,
			class_balance=False, min_representation_percentage=min_rep_percent,
			class_expansion=class_expansion)
		map_func = functools.partial(gen_map, feature_length=self.feature_length, 
									samples=self.samples)
		train_dataset = train_dataset.batch(self.batch_size, drop_remainder=False)
		train_dataset = train_dataset.map(map_func)
		train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)
		train_dataset = train_dataset.unbatch()
		train_dataset = train_dataset.cache()
		val_dataset = val_dataset.batch(self.batch_size, drop_remainder=False)
		val_dataset = val_dataset.map(map_func)
		val_dataset = val_dataset.prefetch(tf.data.AUTOTUNE)
		val_dataset = val_dataset.unbatch()
		val_dataset = val_dataset.cache()

		loss_fn = tf.losses.SparseCategoricalCrossentropy()
		metrics = [tf.metrics.SparseCategoricalAccuracy()]
		optimizer = tf.keras.optimizers.Adam(lr, decay=lr_decay)
		self.model.compile(optimizer=optimizer, loss=loss_fn, metrics=metrics)
		self.model.fit(train_dataset, epochs=epochs, validation_data=val_dataset, 
						callbacks=self.callbacks)
		self.model = tf.keras.models.load_model(self.checkpoint_path+'loss_optim')

	def pred(self, samples):
		if(len(samples) > 1):
			#Use model.predict
			if(isinstance(samples, list)):
				samples = np.array(samples)
			else:
				pass
			predictions = self.model.predict(samples)
		else:
			predictions = [self.model(tf.convert_to_tensor(samples), training=False)]
		return predictions

	def eval(self, samples, confidence=0.80):
		map_func = functools.partial(gen_map, 
			feature_length=self.feature_length, samples=self.samples)
		print('Batch size: {}'.format(self.batch_size))
		eval_dataset = CryptoDataset(samples, batch_size=self.batch_size, 
			feature_length=self.feature_length, samples=self.samples, 
			stride_length=self.stride_length*5, lookahead=self.lookahead, 
			gain_threshold=self.gain_threshold, loss_threshold=self.loss_threshold, 
			training=False, class_expansion=False, class_balance=False)
		eval_dataset = eval_dataset.batch(self.batch_size, drop_remainder=False)
		eval_dataset = eval_dataset.map(map_func)
		eval_dataset = eval_dataset.prefetch(tf.data.AUTOTUNE)
		eval_dataset = eval_dataset.unbatch()
		eval_dataset = eval_dataset.cache()
		
		y_pred = []
		y_true = []
		for batch_samples, batch_labels in eval_dataset:
			predictions = self.pred(batch_samples)
			y_true.extend(list(batch_labels))
			y_pred.extend(predictions)
		self.y_pred.extend(y_pred)
		self.y_true.extend(y_true)
		self.confidence_matrix(confidence=confidence, y_true=y_true, y_pred=y_pred)
		return (y_true, y_pred)

	def confidence_matrix(self, confidence=0.9, y_true=None, y_pred=None):
		if(y_true is None):
			y_true = self.y_true
		if(y_pred is None):
			y_pred = self.y_pred

		new_y_pred = []
		for prediction in y_pred:
			index = np.argmax(prediction, axis=0)
			if(prediction[index] <= confidence):
				index = 3
			else:
				pass
			new_y_pred.append(index)
		y_pred = new_y_pred

		losses = [label for label in y_true if label == 0]
		neutrals = [label for label in y_true if label == 1]
		gains = [label for label in y_true if label == 2]
		print('True class distribution: loss: {} | neutral: {} | gain: {}'.format(len(losses), len(neutrals), len(gains)))
		y_true = tf.convert_to_tensor(y_true, dtype=tf.float32)
		y_pred = tf.convert_to_tensor(y_pred, dtype=tf.float32)
		confusion_matrix = tf.math.confusion_matrix(y_true, y_pred)
		print('\nConfidence: {}'.format(confidence))
		#print('Poorly formatted Conf Mat: {}'.format(confusion_matrix))
		loss_matrix = confusion_matrix[0]
		neutral_matrix = confusion_matrix[1]
		gain_matrix = confusion_matrix[2]

		if(loss_matrix.shape[0] == 3):
			loss_matrix = tf.concat([loss_matrix, tf.zeros((1,), dtype=tf.int32)], axis=0)
			neutral_matrix = tf.concat([neutral_matrix, tf.zeros((1,), dtype=tf.int32)], axis=0)
			gain_matrix = tf.concat([gain_matrix, tf.zeros((1,), dtype=tf.int32)], axis=0)
		else:
			pass

		loss_matrix = [int(val) for val in loss_matrix]
		neutral_matrix = [int(val) for val in neutral_matrix]
		gain_matrix = [int(val) for val in gain_matrix]

		print('{}| Loss |Neutral| Gain |Unknown|\n_____________________________________\n Loss  |{}|{}|{}|{}|\nNeutral|{}|{}|{}|{}|\n Gain  |{}|{}|{}|{}|\n_____________________________________'.format('T\\P'.center(7, ' '), 
			str(int(loss_matrix[0])).center(6, ' '), str(int(loss_matrix[1])).center(7, ' '), str(int(loss_matrix[2])).center(6, ' '), str(int(loss_matrix[3])).center(7, ' '), 
			str(neutral_matrix[0]).center(6, ' '), str(neutral_matrix[1]).center(7, ' '), str(neutral_matrix[2]).center(6, ' '), str(neutral_matrix[3]).center(7, ' '), 
			str(gain_matrix[0]).center(6, ' '), str(gain_matrix[1]).center(7, ' '), str(gain_matrix[2]).center(6, ' '), str(gain_matrix[3]).center(7, ' ')))	

def create_model(class_count, sequence_length, window_length):
	return LSTMModel(class_count, (sequence_length, window_length))
