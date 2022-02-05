import json
import time
import requests

class AuthManager():
	def __init__(self, auth_key, base_url, max_retries=5):
		self.auth_key = auth_key
		self.base_url = base_url
		self.max_retries = max_retries
		self.endpoint = 'auth/refresh'
		self.request_data = {'apiKey': self.auth_key}
		self.headers = {'Content-Type': 'application/json', 'user-agent': 'urllib3'}
		self.time_delta = 60*60*24
		self.last_renewal_time = 0
		self.access_token = None

	def logout(self, retries=0):
		endpoint = 'auth/logout/'
		headers = self.headers
		headers['Authorization'] = self.access_token
		requests.post(self.base_url+endpoint, data='', headers=headers)
		if(result.status_code != 200):
			if(retries == self.max_retries):
				return 1
			else:
				pass
			return self.logout(retues=retries+1)
		else:
			pass
		return 0

	def refresh(self, retries=0):
		if(self.access_token is None):
			pass
		else:
			self.logout()

		return self.refresh_inner(retries=retries)

	def refresh_inner(self, retries=0):
		
		result = requests.post(self.base_url+self.endpoint, 
							   data=json.dumps(self.request_data),
							   headers=self.headers)
		if(result.status_code != 200):
			print('[Warning] Retryng auth refresh: {}/{}'.format(retries, self.max_retries))
			if(retries == self.max_retries):
				return 0
			else:
				pass
			return self.refresh_inner(retries=retries+1)
		else:
			pass
		returned_json = result.json()
		result.close()

		access_token = returned_json.get('accessToken', None)
		if(access_token is None):
			print('[Warning] No access token was returned')
			if(retries == self.max_retries):
				return 0
			else:
				pass
			return self.refresh_inner(retries=retries+1)
		else:
			pass
		self.access_token = access_token
		self.last_renewal_time = time.time()
		
		return self.access_token

	def get_access_token():
		if(time.time() < self.last_renewal_time + self.time_delta):
			return self.access_token
		else:
			return self.refresh()

class SwyftxAPI():
	def __init__(self, key, demo=True):
		self.demo = demo
		self.demo_url = 'https://api.demo.swyftx.com.au/'
		self.base_url = 'https://api.swyftx.com.au'

		if(os.path.isfile(key)):
			fp = open(key, 'r')
			key = fp.read().split('\n')[0]
			fp.close()
			self.key = key
		else:
			#Assume key is the key
			self.key = key

		self.authman = AuthManager(self.key, self.base_url)
		
	def request(endpoint, headers, data={}, demo=False, retries=0, get=False):
		if(demo and retries != 0):
			endpoint = self.demo_url + endpoint
		elif(retries != 0):
			endpoint = self.base_url + endpoint
		else:
			pass
		data = json.dumps(data)
		
		if(get):
			result = requests.get(endpoint, headers=headers)
		else:
			result = requests.post(endpoint, data=data, headers=headers)
		if(result.status_code != 200):
			if(retries == self.max_retries):
				return 0
			else:
				pass
			retries += 1
			result.close()
			return self.request(endpoint, data, headers, demo=demo, retries=retries)
		else:
			pass

		data = result.json()
		result.close()
		return data 

	#
	#
	# Markets
	#
	#

	def live_rates(self, asset_id):
		#Gets all assets prices against asset_id
		endpoint = 'live-rates/{}/'.format(asset_id)
		headers = {}
		result = self.request(endpoint, headers, get=True)
		return result

	def get_market_assets(self):
		endpoint = 'markets/assets/'
		headers = {}
		result = self.request(endpoint, headers, get=True)
		return result

	def get_basic_info(self, asset_id=None):
		if(asset_id is None):
			endpoint = 'markets/info/basic/'
		else:
			endpoint = 'markets/info/basic/{}/'.format(asset_id)
		headers = {}
		result = self.request(endpoint, headers, get=True)
		return result

	def get_detailed_info(self, asset_id):
		endpoint = 'markets/info/detail/{}/'.format(asset_id)
		headers = {}
		result = self.request(endpoint, headers, get=True)
		return result

	#
	#
	# Info
	#
	#
	
	def get_info(self):
		endpoint = 'info/'
		headers = {}
		result = self.request(endpoint, headers, get=True)
		return result

	#
	#
	# Limits
	#
	#

	def get_withdrawal_limits(self):
		endpoint = 'limits/withdrawal'
		headers = {
					'Content-Type': 'application/json',
					'Authorization': self.authman.get_access_token()
				}
		result = self.request(endpoint, headers, get=True)
		return result

	#
	#
	# Orders
	#
	#
	
	def get_pair_exchange_rate(self, buy_asset_code, sell_asset_code, limit, calc_depth='1000'):
		"""
		The input codes are codes such as USD, AUD, BTC, NZD, ...
		limit is the asset code for whatever currency the exchange rate should be listed in	
		"""
		endpoint = 'orders/rate/'
		data = {'buy': buy_asset_id,
				'sell': sell_asset_id,
				'amount': '1000',
				'limit': limit}
		headers = {
                    'Content-Type': 'application/json',
                    'Authorization': self.authman.get_access_token()
                }
		result = self.request(endpoint, headers, data=data)
		return result

	def get_swap_pair_exchange_rate(self):
		endpoint = 'orders/rate/swap'
		return 'Not implemented'
	def get_pair_exchange_rates(self):
		endpoint = 'orders/rate/swap/multi'
		return 'Not implemented'
	def place_order(self, primary, secondary, quantity, asset_quantity, order_type, trigger, demo=False):
		endpoint = 'orders/'
		data = {'primary': primary,
				'secondary': secondary,
				'quantity': quantity,
				'assetQuantity': asset_quantity,
				'orderType': order_type,
				'trigger': trigger}
		headers = {
                    'Content-Type': 'application/json',
                    'Authorization': self.authman.get_access_token()
                }
		result = self.request(endpoint, headers, data=data)
		return result
	def update_order(self):
		return
	def dust_order(self):
		return 'Not implemented'
	def cancel_order(self):
		return
	def list_orders(self):
		return
	def get_order_by_orderuuid(self):
		return
