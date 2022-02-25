#include <stdbool.h>
#include <stdlib.h>

#include "lstm.h"
#include "matrix.h"

struct matrix_f lstm_4_split(struct matrix_f a, int start, int end) {
	struct matrix_f split = {.x=a.x, .y=a.y/4};
	float *data = (float *)malloc(sizeof(float) * split.x * split.y);
	if(data == NULL) {struct matrix_f fail={0}; return fail;}
	split.data = data;
	//Get all rows but only certain cols
	//Col start and Col end are passed as parameters
	//Easiest way is to transpose and then grab by rows

	struct matrix_f transposed = transpose(a);
	memcpy(split.data, transposed.data+start, end*sizeof(float));
	free(transposed.data);
	transposed = transpose(split);
	free(split.data);

	return transposed;
}

int LSTMCell(struct matrix_f kernel, struct matrix_f recurrent_kernel, 
			 struct matrix_f bias, struct matrix_f x_t, struct matrix_f h_tm1, 
			 struct matrix_f *c_tm1, struct matrix_f *result) {
	struct matrix_f tmp = {0};
	matmul(x_t, kernel, &tmp, false);
	matmul(h_tm1, recurrent_kernel, &tmp, true);
	//Element wise addition
	float *s_t_p = (float *)malloc(sizeof(float) * bias.x * bias.y);
	if(s_t_p == NULL) {return 1;}
	struct matrix_f s_t = {.x=bias.x, .y=bias.y, .data=s_t_p};
	matadd(tmp, bias, &s_t);

	int hunit = recurrent_kernel.x;
	struct matrix_f split_1, split_2, split_3, split_4;
	split_1 = lstm_4_split(s_t, 0, hunit);
	split_2 = lstm_4_split(s_t, 1*hunit, 2*hunit);
	split_3 = lstm_4_split(s_t, 2*hunit, 3*hunit);
	split_4 = lstm_4_split(s_t, 3*hunit, 4*hunit);

	struct matrix_f i, f, _c, o;
	i  = sigmoid(split_1);
	f  = sigmoid(split_2);
	_c = tanh(split_3);
	o  = sigmoid(split_4);

	free(split_1.data);
	free(split_2.data);
	free(split_3.data);
	free(split_4.data);

	matelemul(i, &_c);
	matelemul(f, &c_tm1);

	struct matrix_f c_t;

	matadd(_c, *c_tm1, &c_t); //Final memory for c_t allocated here
	//Element wise multiplication
	float *h_t_p = (float *)malloc(sizeof(float) * c_t.x * c_t.y);
	if(h_t_p == NULL) {return 1;}
	struct matrix_f h_t = {.x=c_t.x, .y=c_t.y, .data=h_t_p};

	h_t = tanh(c_t); //Final memory for result allocated here
	matelemul(o, &h_t); //Does not allocate memory

	
	free(i.data);
	free(f.data);
	free(_c.data);
	free(o.data);
	free(s_t.data);
	free(tmp.data);

	free(c_tm1->data);
	*c_tm1 = c_t;
	*result = h_t;
	
	return 0;//(h_t,c_t);
}

struct lstm_sequence_io_node LSTMLayer(struct lstm_layer layer, 
							struct lstm_sequence_io_node *input, bool return_sequences) {
	
	struct lstm_sequence_io_node result_head = {.next=NULL, .data=NULL};
	struct lstm_sequence_io_node error = {0};

	struct matrix_f h_tm1 = {.x=layer.output_x, .y=layer.output_y};
	float *h_tm1_data = calloc(h_tm1.x*h_tm1.y, sizeof(float));
	if(h_tm1_data == NULL) {return result_head;}

	struct matrix_f c_tm1 = {.x=layer.output_x, .y=layer.output_y};
	float *c_tm1_data = calloc(c_tm1.x*c_tm1.y, sizeof(float));
	if(c_tm1_data == NULL) {return result_head;}
	
	while(input != NULL) {
		struct matrix_f *result = malloc(sizeof(struct matrix_f));

		LSTMCell(*(layer.kernel), *(layer.recurrent_kernel), 
			 *(layer.bias), *(input->data), h_tm1, 
			&c_tm1, result);
		if(return_sequences) {
			if(result_head.data == NULL) {
				result_head.data = result;
			}
			else {
				struct lstm_sequence_io_node *temp = &result_head;
				while(temp->next != NULL) {
					temp = temp->next;
				}
				//temp has the location to insert the new sequence
				struct lstm_sequence_io_node *new = malloc(sizeof(struct lstm_sequence_io_node));
				new->next = NULL;
				new->data = result;
				temp->next = new;
			}
		}
		h_tm1 = *result;
		float *h_tm1_data = malloc(sizeof(float)*h_tm1.x*h_tm1.y);
		if(h_tm1_data == NULL) {return error;}
		h_tm1.data = h_tm1_data;
		memcpy(h_tm1.data, result->data, h_tm1.x*h_tm1.y*sizeof(float));
	}
	
}