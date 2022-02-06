import requests

url = 'https://api.swyftx.com.au/markets/assets/'
headers = {'user-agent': 'bot'}

result = requests.get(url, headers=headers)
result_json = result.json()

#First filter only the wanted assets
unwanted_assets = ['AUD', 'USD', 'NZD', 'GBP', 'EUR', 'JPY']
asset_list = []
for asset in result_json:
	if(asset['assetType'] == 1):
		#Asset type 1 is fiat currency
		continue
	tether = False
	for unwanted in unwanted_assets:
		if(unwanted in asset['code']):
			tether = True
	if(tether):
		#Catch tether coins
		continue
	if(asset['code'][0].isdigit()):
		continue
	else:
		asset_list.append(asset)

#assets.py

print('\n\n############################################################################\n//assets.py\n############################################################################\n\n')

print('assets = {')

for idx, asset in enumerate(asset_list):
	asset_id = asset['id']
	asset_code = asset['code']
	comma = ','
	if(idx == len(asset_list)-1):
		comma = ''
	print('\t{asset_id}: Asset({asset_id}, \'{asset_code}\', \'{asset_name}\'){comma}'.format(asset_id=asset_id, asset_code=asset_code, asset_name=asset['name'], comma=comma))
print('}')