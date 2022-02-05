import os
import sys
import math
import logging

ASSET_ID_TO_IDX_LUT = [-1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, -1, -1, -1, -1, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, -1, 46, -1, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, -1, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, -1, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, -1, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, -1, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, -1, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, -1, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, -1, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, -1, 298, -1, -1, -1, -1, 299, 300, 301, 302, 303, -1, -1, -1, -1, -1, -1, -1, -1, -1, 304, -1, -1, -1, -1, -1, -1, -1, -1, -1, 305]
ASSET_NAMES = ['BTC', 'TRX', 'ETH', 'XRP', 'BCH', 'EOS', 'XVG', 'NEO', 'LTC', 'ADA', 'BNB', 'IOTA', 'QTUM', 'ETC', 'WTC', 'ZRX', 'SUB', 'OMG', 'XMR', 'ZEC', 'BAT', 'LSK', 'SALT', 'FUN', 'MCO', 'POWR', 'VGX', 'WAVES', 'ADX', 'KMD', 'BTT', 'DASH', 'DENT', 'HOT', 'LINK', 'MTL', 'NANO', 'NPXS', 'XLM', 'ZIL', 'SYS', 'PPT', 'VET', 'ONT', 'XEM', 'BTG', 'DCR', 'REP', 'BCD', 'RVN', 'BTS', 'ICX', 'PAX', 'AE', 'SC', 'ATOM', 'STEEM', 'ENJ', 'THETA', 'STRAT', 'SNT', 'GNT', 'ELF', 'ARDR', 'DOGE', 'NXS', 'IOST', 'ZEN', 'MANA', 'XTZ', 'RLC', 'HBAR', 'GAS', 'ONG', 'STX', 'LEND', 'ALGO', 'ENG', 'AGI', 'KNC', 'TNT', 'AION', 'REN', 'WRX', 'HC', 'XZC', 'FTT', 'LRC', 'CHZ', 'WIN', 'BRD', 'FET', 'LTO', 'WABI', 'NKN', 'PERL', 'RCN', 'DATA', 'KAVA', 'GRS', 'OGN', 'COTI', 'ARK', 'SNX', 'ERD', 'COMP', 'BAND', 'DGB', 'BNT', 'DOT', 'FTM', 'IOTX', 'MATIC', 'MFT', 'NULS', 'OCEAN', 'ONE', 'REQ', 'SOL', 'SRM', 'SXP', 'TFUEL', 'EGLD', 'KSM', 'YFI', 'TRB', 'MKR', 'RSR', 'PAXG', 'UNI', 'UMA', 'YFII', 'HIVE', 'STORJ', 'JST', 'IRIS', 'DIA', 'TOMO', 'WAN', 'BZRX', 'ANKR', 'BLZ', 'NMR', 'SAND', 'ARPA', 'CELR', 'VTHO', 'LOOM', 'CVC', 'AST', 'CHR', 'NAS', 'DUSK', 'BAL', 'STPT', 'PNT', 'COCOSOLD', 'FIO', 'KEY', 'DREPOLD', 'CTSI', 'VITE', 'NAV', 'NEBL', 'ANT', 'MDT', 'TCT', 'TROY', 'MBL', 'OXT', 'AVAX', 'SUNOLD', 'SUSHI', 'LUNA', 'WNXM', 'RUNE', 'CRV', 'HNT', 'SCRT', 'ORN', 'UTK', 'XVS', 'AAVE', 'FIL', 'INJ', 'FLM', 'WING', 'ALPHA', 'BEL', 'POLY', 'VIDT', 'BOT', 'NEAR', 'DNT', 'AKRO', 'STRAX', 'GLM', 'GRT', 'GVT', 'QSP', 'CND', 'VIBE', 'WPR', 'QLC', 'MITH', 'COS', 'STMX', 'AVA', 'WBTC', 'MDA', 'AERGO', 'HARD', 'FOR', 'SKL', 'DLT', 'OST', 'PSG', 'JUV', 'MTH', 'OAX', 'EVX', 'VIB', 'RDN', 'BCPT', 'CDT', 'AMB', 'CMT', 'GO', 'CTXC', 'POA', 'ROSE', 'VIA', 'SKY', 'QKC', 'CTK', 'YOYO', 'CELO', 'COCOS', 'FIRO', 'TWT', 'TRU', 'REEF', 'AXS', 'BTCSTOLD', 'SNMOLD', 'APPC', 'IDEX', 'UNFI', 'DODO', 'CAKE', 'RIF', 'NBS', 'FRONT', 'ACM', 'GXS', 'AUCTION', 'BADGER', 'OM', 'LINA', 'BTCST', 'DEGO', 'RAMP', 'PERP', 'LIT', 'TVK', 'FIS', 'PHA', 'ALICE', 'DREP', 'PUNDIX', 'EPS', 'SUPER', 'AUTO', 'ASR', 'GTO', 'CFX', 'SNM', 'SHIB', 'AGIX', 'SUN', 'TORN', 'GTC', 'MDX', 'MASK', 'BAR', 'MIR', 'TLM', 'KEEP', 'ERN', 'LPT', 'QUICK', 'NU', 'POLS', 'FORTH', 'ICP', 'XYM', 'QNT', 'FLOW', 'CKB', 'AR', 'SSV', 'ILV', 'RAY', 'DYDX', 'C98', 'MINA']

class Asset():
	def __init__(self, asset_id, filter_obj):
		self.asset_id = asset_id
		self.in_use = True

		self.__state = 'Startup'
		self.__substate = 'No Data'

		self.filter = filter_obj

		self.ask_prices = []
		self.bid_prices = []
		self.timestamps = []
		self.filtered_ask_prices = []
		self.filtered_bid_prices = []
		self.filtered_timestamps = []

	def set_name(self, asset_name):
		self.asset_name = asset_name

	def add_sample(self, ask_price, bid_price, timestamp):
		#This only gets called if a valid quote came through

		#If max repeated samples reached then cease trading
		if((timestamp - self.timestamps[-1]) > self.max_repeated_samples * self.quote_time_delta):
			#Since stop and limit sells are in place this is safe behavior
			self.__state = 'Inactive'
			self.__substate = 'Max repeated samples reached'
			self.in_use = False
		else:
			pass

		if((timestamp - self.timestamps[-1]) > self.quote_time_delta):
			logging.debug('Repeating {} samples in asset {}'.format(int((timestamp-self.timestamps[-1])/self.quote_time_delta), self.asset_name))
			#Recursive add until timestamp - self.timestamps[-1] is equal to or less than self.quote_time_delta
			self.add_sample(self.ask_prices[-1], self.bid_prices[-1], self.timestamps[-1]+self.quote_time_delta)
		else:
			pass

		self.ask_prices.append(ask_price)
		self.bid_prices.append(bid_price)
		self.timestamps.append(timestamp)

		if(len(self.ask_prices) >= len(self.filter.filter_taps) and len(self.bid_prices) >= len(self.filter.filter_taps)):
			try:
				self.filter.filter(self.ask_prices[-133:])
			except ValueError as e:
				logging.warning('Failed to filter sample! {}'.format(e))
		else:
			pass

def asset_id_in_use(asset_id, assets):
	if(ASSET_ID_TO_IDX_LUT < 0):
		return False
	elif(assets[asset_id].in_use == False):
		return False
	else:
		True
