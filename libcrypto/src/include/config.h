#ifndef CONFIG_H
#define CONFIG_H

#define ARCH_NOARCH

#define QUOTE_TIME_DELTA 5 //Seconds between quotes
#define SAMPLES_PER_MINUTE (60 / QUOTE_TIME_DELTA)
#define WINDOW_LENGTH (SAMPLES_PER_MINUTE * 45) //Length of a single feature given to the LSTM
#define SEQUENCE_LENGTH 8 //There are 8 lots of WINDOW_LENGTH given to the LSTM
#define LOOKAHEAD_LENGTH (SAMPLES_PER_MINUTE * 30) //30 Minute lookahead for classification
#define STRIDE_LENGTH (SAMPLES_PER_MINUTE * 2) //2 Minute stride length

#endif
