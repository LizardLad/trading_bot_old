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