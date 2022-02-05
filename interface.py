import time
import ctypes

assets_p = ctypes.c_void_p()

class FileReader():
	def __init__(self, library_path):
		self.libcrypto = ctypes.CDLL(library_path)
		self.extract_quotes = self.libcrypto.extract_quotes
		self.extract_quotes.restype = ctypes.c_int
		self.extract_quotes.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
		
		self.get_sample_count = self.libcrypto.get_sample_count
		self.get_sample_count.restype = ctypes.c_uint
		self.get_sample_count.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_bool]
		
		self.get_timestamps = self.libcrypto.get_timestamps
		self.get_timestamps.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_bool, ctypes.c_void_p, ctypes.c_uint];
		
		self.get_asset_samples = self.libcrypto.get_asset_samples
		self.get_asset_samples.restype = ctypes.c_int
		self.get_asset_samples.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint]
		
		self.free_asset_buffer = self.libcrypto.free_asset_buffer
		self.free_asset_buffer.argtypes = [ctypes.c_void_p]
		
		self.get_record_count = self.libcrypto.get_record_count
		self.get_record_count.restype = ctypes.c_uint
		self.get_record_count.argtypes = [ctypes.c_char_p]

	def read_from_file(self, filename):
		filename = ctypes.create_string_buffer(filename.encode('utf-8'))
		num_records = self.get_record_count(filename)
		result = self.extract_quotes(filename, ctypes.byref(assets_p))
		self.assets_p = assets_p
		return result

	def get_filtered_ask_prices_from_asset_id(self, asset_id):
		sample_count = self.get_sample_count(self.assets_p, ctypes.c_uint(asset_id), ctypes.c_bool(True))
		d_buffer = (ctypes.c_double * sample_count)()
		self.get_asset_samples(self.assets_p, ctypes.c_uint(asset_id), None, None, None, ctypes.byref(d_buffer), None, None, sample_count)
		return list(d_buffer)

	def get_filtered_timestamps(self, asset_id):
		sample_count = self.get_sample_count(self.assets_p, ctypes.c_uint(asset_id), ctypes.c_bool(True))
		i_buffer = (ctypes.c_longlong * sample_count)()
		sample_count = self.get_timestamps(assets_p, ctypes.c_uint(asset_id), ctypes.c_bool(True), ctypes.byref(i_buffer), sample_count)
		return list(i_buffer)

	def free(self):
		self.free_asset_buffer(assets_p)

if __name__ == '__main__':
	filename = '/home/oliver/Datasets/crypto/raw/train_val/swyftx-live-data-1631512055'
	start_time = time.time()
	reader = FileReader('../libcrypto.so')
	reader.read_from_file(filename)
	print(reader.get_filtered_timestamps(3))
	reader.get_filtered_ask_prices_from_asset_id(3)
	print('Duration: {}'.format(time.time()-start_time))
