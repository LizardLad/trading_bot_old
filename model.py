import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Model
from tensorflow.keras.layers import LSTM, Dropout, Dense

class LSTMModel(Model):
	def __init__(self, class_count, input_dim, **kwargs):
		super(LSTMModel, self).__init__(**kwargs)
		self.lstm_1 = LSTM(640, input_shape=input_dim, return_sequences=True)
		self.lstm_2 = LSTM(400, return_sequences=True, dropout=0.3)
		self.lstm_3 = LSTM(256, return_sequences=True, dropout=0.3)
		self.lstm_4 = LSTM(256, dropout=0.1)

		self.linear_1 = Dense(512, activation='relu')
		self.dropout_1 = Dropout(0.3)
		self.linear_2 = Dense(256, activation='relu')
		self.dropout_2 = Dropout(0.3)
		self.linear_3 = Dense(128, activation='relu')
		self.dropout_3 = Dropout(0.3)
		self.linear_4 = Dense(64, activation='relu')
		self.dropout_4 = Dropout(0.2)
		self.linear_5 = Dense(16, activation='relu')

		if class_count == 1:
			self.outputs = Dense(class_count)
		else:
			self.outputs = Dense(class_count, activation='softmax')

	def call(self, x):
		x = self.lstm_1(x)
		x = self.lstm_2(x)
		x = self.lstm_3(x)
		x = self.lstm_4(x)
		
		x = self.linear_1(x)
		x = self.dropout_1(x)
		x = self.linear_2(x)
		x = self.dropout_2(x)
		x = self.linear_3(x)
		x = self.dropout_3(x)
		x = self.linear_4(x)
		x = self.dropout_4(x)
		x = self.linear_5(x)
		
		x = self.outputs(x)
		return x
