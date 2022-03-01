#ifndef ACTIVATIONS_H
#define ACTIVATIONS_H

#include "matrix.h"

void noop(struct matrix_f *a);
void relu(struct matrix_f *a);
void softmax(struct matrix_f *a);

#endif