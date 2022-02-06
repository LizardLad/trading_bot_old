#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>

#include "include/extract.h"
#include "include/assets.h"
#include "include/filter.h"

int extract_quotes(char *filename, struct asset_t **assets_ret) {
	//Get number of bytes required to alloc
	struct asset_t *assets;
	size_t buffer_size = sizeof(struct asset_t) * ASSETS_LENGTH;
	assets = (struct asset_t *)malloc(buffer_size);
	if(assets == NULL) {
		return -1;
	}
	uint32_t record_count = get_record_count(filename);
	init_asset_list(assets, record_count);

	int ret = read_in_asset_samples(filename, assets, record_count);
	if(ret) {
		fprintf(stderr, "Read in asset samples error occured! %d\n", ret);
		return ret;
	}
	for(int i = 0; i < ASSETS_LENGTH; i++) {
		if(assets[i].in_use == true)
			filter_data(&(assets[i]));
		if(assets[i].filtered_sample_count == 0) //If there are no filtered samples then don't use it
			assets[i].in_use = false;
	}
	*assets_ret = assets;
	return 0;
}

void free_asset_buffer(struct asset_t *assets) {
	free_assets(assets);
}

int main() {
	//Just for a valgrind test
	struct asset_t *assets;
	extract_quotes("test_file", &assets);
	free_asset_buffer(assets);
}