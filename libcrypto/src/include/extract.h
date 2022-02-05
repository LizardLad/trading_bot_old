#ifndef EXTRACT_H
#define EXTRACT_H

#include <stdint.h>
#include <stdbool.h>
#include "config.h"

//#define SAMPLES_PER_HOUR (60*60/QUOTE_TIME_DELTA)
//#define HOURS_PER_YEAR (365*24/3)
#define SAMPLES_PER_HOUR (60*30/QUOTE_TIME_DELTA)
#define HOURS_PER_YEAR (365)

struct packet_header
{
	uint32_t length;
	uint32_t sample_timestamp;
};

/*struct asset_t
{
	double ask_prices[SAMPLES_PER_HOUR*HOURS_PER_YEAR];
	double mid_prices[SAMPLES_PER_HOUR*HOURS_PER_YEAR];
	double bid_prices[SAMPLES_PER_HOUR*HOURS_PER_YEAR];
	double filtered_ask_prices[SAMPLES_PER_HOUR*HOURS_PER_YEAR];
	double filtered_mid_prices[SAMPLES_PER_HOUR*HOURS_PER_YEAR];
	double filtered_bid_prices[SAMPLES_PER_HOUR*HOURS_PER_YEAR];
	int64_t timestamps[SAMPLES_PER_HOUR*HOURS_PER_YEAR];
	int64_t *filtered_timestamps; //Size is ((SAMPLES_PER_HOUR*HOURS_PER_YEAR) - FILTER_TAP_LENGTH)
	uint32_t sample_count; //How many to read from prices and timestamps
	uint32_t filtered_sample_count;
	bool in_use;
	const char *token_name;
	uint32_t token_id;
	//Add to this later
};*/

struct asset_t
{
	double *ask_prices;
	double *mid_prices;
	double *bid_prices;
	double *filtered_ask_prices;
	double *filtered_mid_prices;
	double *filtered_bid_prices;
	int64_t *timestamps;
	int64_t *filtered_timestamps; //Size is ((SAMPLES_PER_HOUR*HOURS_PER_YEAR) - FILTER_TAP_LENGTH)
	uint32_t sample_count; //How many to read from prices and timestamps
	uint32_t filtered_sample_count;
	bool in_use;
	const char *token_name;
	uint32_t token_id;
	//Add to this later
};

int insert_latest_quote(struct asset_t *dest_asset, double mid_price, double ask_price, double bid_price, int64_t timestamp, uint32_t record_count);
int update_asset_quotes(uint8_t *json, struct asset_t *assets, int64_t timestamp, uint32_t record_count);
/*int backtrack_to_char(char *str, char val);*/
int inflate_buffer(uint8_t *input, uint64_t input_length, uint8_t *output, uint64_t output_length);
char *zerr(int ret);
int read_from_input(uint8_t *ptr, uint64_t count, uint64_t size, uint8_t *source, uint64_t input_length);
int read_in_asset_samples(char *filename, struct asset_t *assets, uint32_t record_count);
unsigned int get_record_count(char *filename);

#endif
