#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "matrix.h"

void noop(struct matrix_f *a) {
	return;
}

void relu(struct matrix_f *a) { //Could do with OpenMP speedup
	for(int i = 0; i < a->x; i++) {
		for(int j = 0; j < a->y; j++) {
			if(a->data[i*a->y+j] < 0) a->data[i*a->y+j] = 0;
		}
	}
}

void softmax(struct matrix_f *a) {
	//Only implemented for 2D array with [[a, b, c, ..., z]] shape where len of outer layer
	//is 1
	if(a->x != 1) {
		return;
	}
	float sum = 0;
	for(int j = 0; j < a->y; j++) {
		sum += expf(a->data[j]);
	}
	for(int j = 0; j < a->y; j++) {
		a->data[j] = (expf(a->data[j]))/sum;
	}
}