#ifndef FILTER_H
#define FILTER_H

#include "extract.h"

#define FILTER_TAP_LENGTH 133
extern const double filter_taps[FILTER_TAP_LENGTH];
void filter_data(struct asset_t *token);
void apply_filter(double *input, double *output);

#endif
