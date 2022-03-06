#ifndef LSTM_H
#define LSTM_H

#include <stdbool.h>
#include "matrix.h"

struct lstm_layer {
	int input_x;
	int input_y;
	struct matrix_f *kernel;
	struct matrix_f *recurrent_kernel;
	struct matrix_f *bias;
	int output_x;
	int output_y;
	bool return_sequences;
};

struct lstm_sequence_io_node {
	struct lstm_sequence_io_node *next;
	struct matrix_f *data;
};

struct lstm_sequence_io_node LSTMLayer(struct lstm_layer layer, struct lstm_sequence_io_node *input);
void free_lstm_sequence(struct lstm_sequence_io_node *sequence);

#endif