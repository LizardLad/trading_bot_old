#include <assert.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <byteswap.h>
#include <endian.h>
#include <ctype.h>
#include <zlib.h>

#include "include/extract.h"
#include "include/assets.h"
#include "include/json.h"

//Set the ZLIB buffer size
#define CHUNK (1<<18) // 256K as suggested by ZLIB documentation
static uint8_t json_output[CHUNK];

char *zerr(int ret) {
	char *error = NULL;
	switch(ret) {
		case Z_ERRNO:
			if(ferror(stdin))
				error = "Error reading stdin";
			if(ferror(stdout))
				error = "Error writing stdout";
			break;
		case Z_STREAM_ERROR:
			error = "Invalid compression level";
			break;
		case Z_DATA_ERROR:
			error = "Invalid or incomplete deflate data";
			break;
		case Z_MEM_ERROR:
			error = "Out of memory";
			break;
		case Z_VERSION_ERROR:
			error = "ZLIB version mismatch";
			break;
		default:
			error = "Unknown error";
	}
	return error;
}

int inflate_buffer(uint8_t *input, uint64_t input_length, uint8_t *output, uint64_t output_length) {
	int32_t ret;
	uint32_t have;
	z_stream stream;

	stream.zalloc = Z_NULL;
	stream.zfree = Z_NULL;
	stream.opaque = Z_NULL;
	stream.avail_in = 0;
	stream.next_in = Z_NULL;
	ret = inflateInit(&stream);
	if(ret != Z_OK){return ret;}
	
	stream.avail_in = input_length;
	if(stream.avail_in == 0){return INT_MAX;}
		
	stream.next_in = input;
	stream.avail_out = output_length;
	stream.next_out = output;
	ret = inflate(&stream, Z_NO_FLUSH);
	switch(ret) {
		case Z_OK:
		case Z_STREAM_END:
			break;
		default:
			(void)inflateEnd(&stream);
			return ret;
	}

	(void)inflateEnd(&stream);
	if(ret != Z_STREAM_END || stream.avail_out == 0)
		return -INT_MAX;
	
	have = output_length - stream.avail_out;
	output[have] = '\0';
	return Z_OK;
}

bool is_string_number(char *s) {
	while(*s != '\0') {
		if(!isdigit(*s)) {return false;};
		s++;
	}
	return true;
}

int extract_price_data_json(const char *json, struct json_token *tokens, int num_tokens, int parent_node, double *ask_price, double *mid_price, double *bid_price) {
	int ask_price_token_id = -2;
	int mid_price_token_id = -2;
	int bid_price_token_id = -2;
	bool found_ask_price = false;
	bool found_mid_price = false;
	bool found_bid_price = false;
	for(int i = parent_node; i < num_tokens && (!found_ask_price || !found_mid_price || !found_bid_price); i++) {
		if(tokens[tokens[i].parent].parent == parent_node) {
			if(!strncmp("askPrice", &(json[tokens[i].start]), 8)) {
				ask_price_token_id = i;
			}
			if(!strncmp("midPrice", &(json[tokens[i].start]), 8)) {
				mid_price_token_id = i;
			}
			if(!strncmp("bidPrice", &(json[tokens[i].start]), 8)) {
				bid_price_token_id = i;
			}
		}
		if(tokens[i].parent == ask_price_token_id) {
			*ask_price = strtod(&(json[tokens[i].start]), NULL);
			found_ask_price = true;
		}
		if(tokens[i].parent == mid_price_token_id) {
			*mid_price = strtod(&(json[tokens[i].start]), NULL);
			found_mid_price = true;
		}
		if(tokens[i].parent == bid_price_token_id) {
			*bid_price = strtod(&(json[tokens[i].start]), NULL);
			found_bid_price = true;
		}
	}
	if(found_ask_price && found_mid_price && found_bid_price) {
		return 0;
	}
	return 1;
}

int update_asset_quotes(uint8_t *json, struct asset_t *assets, int64_t timestamp, uint32_t record_count) {
	struct json_parser parser;
	struct json_token tokens[2*4096];
	json_init(&parser);

	int token_count = json_parse(&parser, (char *)json, strlen((char *)json), tokens, 2*4096);
	if(token_count < 0){fprintf(stderr, "Some sort of error occured parsing the JSON: %d\n", token_count);return 1;}

	int asset_id_to_token_id[HIGHEST_ASSET_ID+1];
	for(int i=0;i<HIGHEST_ASSET_ID+1;i++){asset_id_to_token_id[i]=-1;}

	for(int i = 0; i < token_count; i++) {
		if(tokens[i].parent == 0)
		{
			//This is the asset_id
			char temp = json[tokens[i].end];
			json[tokens[i].end] = '\0';
			if(is_string_number((char *)&json[tokens[i].start]))
			{
				int asset_id = atoi((char *)&json[tokens[i].start]);
				if(asset_id <= HIGHEST_ASSET_ID)
				{
					if(asset_exists(asset_id))
					{
						asset_id_to_token_id[asset_id] = i;
					}
				}
				continue;
			}
			json[tokens[i].end] = temp;
		}
	}

	for(int i = 0; i < HIGHEST_ASSET_ID+1; i++)
	{
		if(asset_id_to_token_id[i] != -1)
		{
			int parent_node = asset_id_to_token_id[i];
			double ask_price, mid_price, bid_price;
			int ret = extract_price_data_json((char *)json, tokens, token_count, parent_node, &ask_price, &mid_price, &bid_price);
			int asset_index = asset_id_lut(i);
			if(ret)
			{
				//Missed a sample
				assets[asset_index].in_use = false;
				continue;
			}
			if(insert_latest_quote(&(assets[asset_index]), mid_price, ask_price, bid_price, timestamp, record_count))
			{
				//If there is no remaining space
				return 2;
			}
		}
	}
	return 0;
}

int insert_latest_quote(struct asset_t *dest_asset, double mid_price, double ask_price, double bid_price, int64_t timestamp, uint32_t record_count)
{
	if(dest_asset->sample_count < record_count)
	{
			//Put it in here
			dest_asset->ask_prices[dest_asset->sample_count] = ask_price;
			dest_asset->mid_prices[dest_asset->sample_count] = mid_price;
			dest_asset->bid_prices[dest_asset->sample_count] = bid_price;
			dest_asset->timestamps[dest_asset->sample_count] = timestamp;
			(dest_asset->sample_count)++;
			return 0;
	}
	return 1;
}

unsigned int get_record_count(char *filename) {
	FILE *input_file = fopen(filename, "rb");
	unsigned int count = 0;
	while(!feof(input_file)) {
		count++;
		struct packet_header header;
		size_t bytes_read = fread(&header, 1, 8, input_file);
		if(bytes_read != 8) {
			if(feof(input_file)) {
				break;
			} else {
				fclose(input_file);
				return 0;
			}
		}
		header.length = be32toh(header.length);
		if(fseek(input_file, header.length, SEEK_CUR) != 0) {
			if(feof(input_file)) {
				break;
			} else {
				fclose(input_file);
				return 0;
			}
		}
	}
	fclose(input_file);
	return count;
}

int read_in_asset_samples(char *filename, struct asset_t *assets, uint32_t record_count)
{
	FILE *input_file = fopen(filename, "rb");
	while(!feof(input_file))
	{
		struct packet_header header;
		size_t bytes_read_header = fread(&header, 1, 8, input_file);
		if(bytes_read_header != 8) {
			if(feof(input_file)) {
				break;
			} else {
				return INT_MAX;
			}
		}

		header.length = be32toh(header.length);
		header.sample_timestamp = be32toh(header.sample_timestamp);

		uint8_t *compressed_chunk = malloc(header.length);
		size_t bytes_read = fread(compressed_chunk, 1, header.length, input_file);
		if(bytes_read != header.length) {
			free(compressed_chunk);
			if(feof(input_file)) {
				break;
			} else {
				return INT_MAX;
			}
		}

		int32_t ret = inflate_buffer(compressed_chunk, header.length, json_output, CHUNK);
		if(ret != Z_OK) {
			fprintf(stderr, "[ERROR] ZLIB error\n");
			fprintf(stderr, "[ERROR] errno: %d\n", ret);
			fprintf(stderr, "[ERROR] error: %s\n", zerr(ret));
			free(compressed_chunk);
			fclose(input_file);
			return ret;
		}	
		free(compressed_chunk);
		
		//At each timestep add the new quotes to the assets		
		ret = update_asset_quotes(json_output, assets, header.sample_timestamp, record_count);
		if(ret)
		{
			//No remaining space
			printf("Error occured\n");
			fclose(input_file);
			return ret;
		}

	}
	fclose(input_file);
	return 0;
}

unsigned int get_sample_count(struct asset_t *assets, unsigned int token_id, bool filtered)
{
	if(asset_exists(token_id)) {
		if(assets[asset_id_lut(token_id)].in_use) {
			if(filtered) {
				return assets[asset_id_lut(token_id)].filtered_sample_count;
			} else {
				return assets[asset_id_lut(token_id)].sample_count;
			}
		}
	}
	return 0;
}

void get_timestamps(struct asset_t *assets, unsigned int token_id, bool filtered, int64_t *dst, unsigned int sample_count) {
	unsigned int max_samples = get_sample_count(assets, token_id, false);
	unsigned int max_filtered_samples = get_sample_count(assets, token_id, true);
	if(filtered) {
		max_samples = (sample_count < max_filtered_samples) ? sample_count: max_filtered_samples;
	} else {
		max_samples = (sample_count < max_samples) ? sample_count : max_samples;
	}

	if(filtered) {
		memcpy(dst, assets[asset_id_lut(token_id)].filtered_timestamps, sizeof(int64_t)*max_samples);
	} else {
		memcpy(dst, assets[asset_id_lut(token_id)].timestamps, sizeof(int64_t)*max_samples);
	}
}

int get_asset_samples(struct asset_t *assets, unsigned int token_id, double *ask_prices, double *mid_prices, double *bid_prices, double *filtered_ask_prices, double *filtered_mid_prices, double *filtered_bid_prices, unsigned int sample_count)
{
	double *src;
	unsigned int max_samples = get_sample_count(assets, token_id, false);
	unsigned int max_filtered_samples = get_sample_count(assets, token_id, true);
	if((filtered_ask_prices != NULL || filtered_mid_prices != NULL || filtered_bid_prices != NULL) && max_filtered_samples == 0) {
		return -1;	
	}
	if(max_samples == 0) {
		return -2;
	}
	struct asset_t *asset = &(assets[asset_id_lut(token_id)]);
	if(ask_prices != NULL) {
		src = asset->ask_prices;
		memcpy(ask_prices, src, sizeof(double)*((sample_count < max_samples) ? sample_count : max_samples));
	}
	if(mid_prices != NULL) {
		src = asset->mid_prices;
		memcpy(mid_prices, src, sizeof(double)*((sample_count < max_samples) ? sample_count : max_samples));
	}
	if(bid_prices != NULL) {
		src = asset->bid_prices;
		memcpy(bid_prices, src, sizeof(double)*((sample_count < max_samples) ? sample_count : max_samples));
	}
	if(filtered_ask_prices != NULL) {
		src = asset->filtered_ask_prices;
		memcpy(filtered_ask_prices, src, sizeof(double)*((sample_count < max_filtered_samples) ? sample_count : max_filtered_samples));
	}
	if(filtered_mid_prices != NULL) {
		src = asset->filtered_mid_prices;
		memcpy(filtered_mid_prices, src, sizeof(double)*((sample_count < max_filtered_samples) ? sample_count : max_filtered_samples));
	}
	if(filtered_bid_prices != NULL) {
		src = asset->filtered_bid_prices;
		memcpy(filtered_bid_prices, src, sizeof(double)*((sample_count < max_filtered_samples) ? sample_count : max_filtered_samples));
	}
	return 0;
}
