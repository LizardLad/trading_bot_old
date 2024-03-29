import os
import sys
import math
import filter
import logging

from config import cfg

class Asset():
	def __init__(self, asset_id, asset_code, asset_name):
		self.asset_id = asset_id
		self.asset_code = asset_code
		self.asset_name = asset_name

		self.__state = 'Startup'
		self.__substate = 'No Data'

		self.filter = filter.Filter()

		self.max_repeated_samples = int(cfg.get('max_repeated_samples', 10))
		self.quote_time_delta = int(cfg.get('quote_time_delta', 5))

		self.raw_history = []
		self.filtered_history = []

	def add_samples_from_file(self, ask_price_samples, mid_price_samples, bid_price_samples, timestamps, filtered=False):
		for i, ask_price in enumerate(ask_price_samples):
			mid_price = mid_price_samples[i]
			bid_price = bid_price_samples[i]
			timestamp = timestamps[i]
			sample = {
				'ask_price': ask_price,
				'mid_price': mid_price,
				'bid_price': bid_price,
				'timestamp': timestamp
			}
			if(filtered):
				self.filtered_history.append(sample)
			else:
				self.raw_history.append(sample)


	def add_sample(self, ask_price, mid_price, bid_price, timestamp): #This only gets called if a valid quote came through
		#If number of duplicate samples required is greater than max_repeated_samples
		if((timestamp - self.timestamps[-1]) > (self.max_repeated_samples * self.quote_time_delta)):
			#Since stop and limit sells are in place this is safe behavior
			self.__state = 'Inactive'
			self.__substate = 'Max repeated samples reached'
		elif((timestamp - self.timestamps[-1]) > self.quote_time_delta):
			logging.debug('Repeating {} samples in asset {}'.format(int((timestamp-self.timestamps[-1])/self.quote_time_delta), self.asset_name))
			#Recursive add until timestamp - self.timestamps[-1] is equal to or less than self.quote_time_delta
			self.add_sample(self.raw_history[-1]['ask_price'],
				self.raw_history[-1]['mid_price'],
				self.raw_history[-1]['bid_price'],
				self.raw_history[-1]['timestamp']+self.quote_time_delta)

		#Valid raw sample
		raw_sample = {
			'ask_price': ask_price,
			'mid_price': mid_price,
			'bid_price': bid_price,
			'timestamp': timestamp
		}
		self.raw_history.append(raw_sample)

		if(len(self.raw_history) >= len(self.filter.filter_taps)):
			try:
				filtered_sample = self.filter.filter(self.raw_history[-self.filter.filter_taps:])
				self.filtered_history.append(filtered_sample)
			except ValueError as e:
				logging.warning('Failed to filter sample! {}'.format(e))

	def get_samples(self, filtered=True, side='ask'):
		history = self.filtered_history if filtered else self.raw_history
		samples = []
		for historical_sample in history:
			if(side == 'ask'):
				samples.append(historical_sample['ask_price'])
			elif(side == 'mid'):
				samples.append(historical_sample['mid_price'])
			elif(side == 'bid'):
				samples.append(historical_sample['bid_price'])
			else:
				raise ValueError('Asset.get_samples invalid side requested')
		return samples

assets = {
        3: Asset(3, 'BTC', 'Bitcoin'),
        4: Asset(4, 'TRX', 'TRON'),
        5: Asset(5, 'ETH', 'Ethereum'),
        6: Asset(6, 'XRP', 'XRP'),
        7: Asset(7, 'BCH', 'Bitcoin Cash'),
        8: Asset(8, 'EOS', 'EOS'),
        9: Asset(9, 'XVG', 'Verge'),
        10: Asset(10, 'NEO', 'NEO'),
        11: Asset(11, 'LTC', 'Litecoin'),
        12: Asset(12, 'ADA', 'Cardano'),
        13: Asset(13, 'BNB', 'Binance Coin'),
        14: Asset(14, 'IOTA', 'IOTA'),
        15: Asset(15, 'QTUM', 'Qtum'),
        16: Asset(16, 'ETC', 'Ethereum Classic'),
        17: Asset(17, 'WTC', 'Waltonchain'),
        18: Asset(18, 'ZRX', '0x'),
        19: Asset(19, 'SUB', 'Substratum'),
        20: Asset(20, 'OMG', 'OMG Network'),
        21: Asset(21, 'XMR', 'Monero'),
        22: Asset(22, 'ZEC', 'Zcash'),
        23: Asset(23, 'BAT', 'Basic Attention Token'),
        24: Asset(24, 'LSK', 'Lisk'),
        25: Asset(25, 'SALT', 'SALT'),
        26: Asset(26, 'FUN', 'FunFair'),
        27: Asset(27, 'MCO', 'Monaco'),
        28: Asset(28, 'POWR', 'Power Ledger'),
        29: Asset(29, 'VGX', 'Voyager'),
        30: Asset(30, 'WAVES', 'Waves'),
        31: Asset(31, 'ADX', 'AdEx'),
        32: Asset(32, 'KMD', 'Komodo'),
        37: Asset(37, 'BTT', 'BitTorrent'),
        38: Asset(38, 'DASH', 'Dash'),
        39: Asset(39, 'DENT', 'Dent'),
        40: Asset(40, 'HOT', 'Holo'),
        41: Asset(41, 'LINK', 'Chainlink'),
        42: Asset(42, 'MTL', 'Metal'),
        43: Asset(43, 'NANO', 'Nano'),
        44: Asset(44, 'NPXS', 'Pundi X'),
        45: Asset(45, 'XLM', 'Stellar Lumens'),
        46: Asset(46, 'ZIL', 'Zilliqa'),
        47: Asset(47, 'SYS', 'Syscoin'),
        48: Asset(48, 'PPT', 'Populous'),
        49: Asset(49, 'VET', 'VeChain'),
        50: Asset(50, 'ONT', 'Ontology'),
        51: Asset(51, 'XEM', 'NEM'),
        52: Asset(52, 'BTG', 'Bitcoin Gold'),
        54: Asset(54, 'DCR', 'Decred'),
        56: Asset(56, 'REP', 'Augur'),
        57: Asset(57, 'BCD', 'Bitcoin Diamond'),
        58: Asset(58, 'RVN', 'Ravencoin'),
        59: Asset(59, 'BTS', 'BitShares'),
        60: Asset(60, 'ICX', 'ICON'),
        61: Asset(61, 'PAX', 'Paxos Standard Token'),
        62: Asset(62, 'AE', 'Aeternity'),
        63: Asset(63, 'SC', 'Siacoin'),
        64: Asset(64, 'ATOM', 'Cosmos'),
        65: Asset(65, 'STEEM', 'Steem'),
        66: Asset(66, 'ENJ', 'Enjin Coin'),
        67: Asset(67, 'THETA', 'THETA'),
        68: Asset(68, 'STRAT', 'Stratis'),
        69: Asset(69, 'SNT', 'Status'),
        70: Asset(70, 'GNT', 'Golem'),
        71: Asset(71, 'ELF', 'aelf'),
        72: Asset(72, 'ARDR', 'Ardor'),
        73: Asset(73, 'DOGE', 'Dogecoin'),
        74: Asset(74, 'NXS', 'Nexus'),
        75: Asset(75, 'IOST', 'IOST'),
        76: Asset(76, 'ZEN', 'Horizen'),
        77: Asset(77, 'MANA', 'Decentraland'),
        79: Asset(79, 'XTZ', 'Tezos'),
        80: Asset(80, 'RLC', 'iExec RLC'),
        81: Asset(81, 'HBAR', 'Hedera Hashgraph'),
        82: Asset(82, 'GAS', 'Gas'),
        83: Asset(83, 'ONG', 'Ontology Gas'),
        84: Asset(84, 'STX', 'Stacks'),
        85: Asset(85, 'LEND', 'Aave'),
        86: Asset(86, 'ALGO', 'Algorand'),
        87: Asset(87, 'ENG', 'Enigma'),
        88: Asset(88, 'AGI', 'SingularityNET'),
        89: Asset(89, 'KNC', 'Kyber Network'),
        90: Asset(90, 'TNT', 'Tierion'),
        91: Asset(91, 'AION', 'Aion'),
        92: Asset(92, 'REN', 'Ren'),
        93: Asset(93, 'WRX', 'WazirX'),
        94: Asset(94, 'HC', 'HyperCash'),
        96: Asset(96, 'XZC', 'ZCoin'),
        97: Asset(97, 'FTT', 'FTX Token'),
        98: Asset(98, 'LRC', 'Loopring'),
        99: Asset(99, 'CHZ', 'Chiliz'),
        100: Asset(100, 'WIN', 'WINk'),
        101: Asset(101, 'BRD', 'Bread'),
        102: Asset(102, 'FET', 'Fetch.ai'),
        103: Asset(103, 'LTO', 'LTO Network'),
        104: Asset(104, 'WABI', 'Tael'),
        105: Asset(105, 'NKN', 'NKN'),
        106: Asset(106, 'PERL', 'Perlin'),
        107: Asset(107, 'RCN', 'Ripio Credit Network'),
        108: Asset(108, 'DATA', 'Streamr DATAcoin'),
        109: Asset(109, 'KAVA', 'Kava'),
        110: Asset(110, 'GRS', 'Groestlcoin'),
        111: Asset(111, 'OGN', 'Origin Protocol'),
        112: Asset(112, 'COTI', 'COTI'),
        113: Asset(113, 'ARK', 'Ark'),
        115: Asset(115, 'SNX', 'Synthetix Network Token'),
        116: Asset(116, 'ERD', 'Elrond'),
        117: Asset(117, 'COMP', 'Compound'),
        118: Asset(118, 'BAND', 'BAND'),
        119: Asset(119, 'DGB', 'DigiByte'),
        120: Asset(120, 'BNT', 'Bancor'),
        121: Asset(121, 'DOT', 'Polkadot'),
        122: Asset(122, 'FTM', 'Fantom'),
        123: Asset(123, 'IOTX', 'IoTeX'),
        124: Asset(124, 'MATIC', 'Polygon'),
        125: Asset(125, 'MFT', 'Mainframe'),
        126: Asset(126, 'NULS', 'Nuls'),
        127: Asset(127, 'OCEAN', 'Ocean Protocol'),
        128: Asset(128, 'ONE', 'Harmony'),
        129: Asset(129, 'REQ', 'Request Network'),
        130: Asset(130, 'SOL', 'Solana'),
        131: Asset(131, 'SRM', 'Serum'),
        132: Asset(132, 'SXP', 'Swipe'),
        133: Asset(133, 'TFUEL', 'Theta Fuel'),
        134: Asset(134, 'EGLD', 'Elrond eGold'),
        135: Asset(135, 'KSM', 'Kusama'),
        136: Asset(136, 'YFI', 'yearn.finance'),
        137: Asset(137, 'TRB', 'Tellor'),
        138: Asset(138, 'MKR', 'Maker'),
        139: Asset(139, 'RSR', 'Reserve Rights'),
        140: Asset(140, 'PAXG', 'PAX Gold'),
        141: Asset(141, 'UNI', 'Uniswap'),
        142: Asset(142, 'UMA', 'UMA'),
        143: Asset(143, 'YFII', 'DFI.Money'),
        144: Asset(144, 'HIVE', 'Hive'),
        145: Asset(145, 'STORJ', 'Storj'),
        146: Asset(146, 'JST', 'JUST'),
        147: Asset(147, 'IRIS', 'IRISnet'),
        148: Asset(148, 'DIA', 'DIA'),
        149: Asset(149, 'TOMO', 'TomoChain'),
        150: Asset(150, 'WAN', 'Wanchain'),
        151: Asset(151, 'BZRX', 'bZx Protocol'),
        152: Asset(152, 'ANKR', 'Ankr'),
        153: Asset(153, 'BLZ', 'Bluzelle'),
        154: Asset(154, 'NMR', 'Numeraire'),
        155: Asset(155, 'SAND', 'The Sandbox'),
        156: Asset(156, 'ARPA', 'ARPA Chain'),
        157: Asset(157, 'CELR', 'Celer Network'),
        158: Asset(158, 'VTHO', 'VeThor Token'),
        159: Asset(159, 'LOOM', 'Loom Network'),
        160: Asset(160, 'CVC', 'Civic'),
        161: Asset(161, 'AST', 'AirSwap'),
        162: Asset(162, 'CHR', 'Chromia'),
        163: Asset(163, 'NAS', 'Nebulas'),
        164: Asset(164, 'DUSK', 'Dusk Network'),
        165: Asset(165, 'BAL', 'Balancer'),
        166: Asset(166, 'STPT', 'Standard Tokenization Protocol'),
        167: Asset(167, 'PNT', 'pNetwork'),
        168: Asset(168, 'COCOSOLD', 'Cocos-BCX Old'),
        169: Asset(169, 'FIO', 'FIO Protocol'),
        170: Asset(170, 'KEY', 'Selfkey'),
        171: Asset(171, 'DREPOLD', 'DREP Old'),
        172: Asset(172, 'CTSI', 'Cartesi'),
        173: Asset(173, 'VITE', 'VITE'),
        174: Asset(174, 'NAV', 'NAV Coin'),
        175: Asset(175, 'NEBL', 'Neblio'),
        176: Asset(176, 'ANT', 'Aragon'),
        177: Asset(177, 'MDT', 'Measurable Data Token'),
        178: Asset(178, 'TCT', 'TokenClub Token'),
        179: Asset(179, 'TROY', 'Troy'),
        180: Asset(180, 'MBL', 'MovieBloc'),
        181: Asset(181, 'OXT', 'Orchid'),
        182: Asset(182, 'AVAX', 'Avalanche'),
        183: Asset(183, 'SUNOLD', 'SUN Old'),
        184: Asset(184, 'SUSHI', 'Sushi'),
        185: Asset(185, 'LUNA', 'Terra'),
        186: Asset(186, 'WNXM', 'Wrapped NXM'),
        187: Asset(187, 'RUNE', 'THORChain'),
        188: Asset(188, 'CRV', 'Curve'),
        189: Asset(189, 'HNT', 'Helium'),
        191: Asset(191, 'SCRT', 'Secret'),
        192: Asset(192, 'ORN', 'Orion Protocol'),
        193: Asset(193, 'UTK', 'Utrust'),
        194: Asset(194, 'XVS', 'Venus'),
        195: Asset(195, 'AAVE', 'Aave'),
        196: Asset(196, 'FIL', 'Filecoin'),
        197: Asset(197, 'INJ', 'Injective Protocol'),
        198: Asset(198, 'FLM', 'Flamingo'),
        199: Asset(199, 'WING', 'Wing Token'),
        200: Asset(200, 'ALPHA', 'Alpha Finance Lab'),
        201: Asset(201, 'BEL', 'Bella Protocol'),
        202: Asset(202, 'POLY', 'Polymath'),
        203: Asset(203, 'VIDT', 'VIDT Datalink'),
        204: Asset(204, 'BOT', 'Bounce Token'),
        205: Asset(205, 'NEAR', 'NEAR Protocol'),
        206: Asset(206, 'DNT', 'district0x'),
        207: Asset(207, 'AKRO', 'Akropolis'),
        208: Asset(208, 'STRAX', 'STRAX Token'),
        209: Asset(209, 'GLM', 'Golem'),
        210: Asset(210, 'GRT', 'The Graph'),
        212: Asset(212, 'GVT', 'Genesis Vision'),
        213: Asset(213, 'QSP', 'Quantstamp'),
        214: Asset(214, 'CND', 'Cindicator'),
        215: Asset(215, 'VIBE', 'VIBE'),
        216: Asset(216, 'WPR', 'WePower'),
        217: Asset(217, 'QLC', 'QLC Chain'),
        218: Asset(218, 'MITH', 'Mithril'),
        219: Asset(219, 'COS', 'Contentos'),
        220: Asset(220, 'STMX', 'StormX'),
        221: Asset(221, 'AVA', 'Travala.com'),
        222: Asset(222, 'WBTC', 'Wrapped Bitcoin'),
        223: Asset(223, 'MDA', 'Moeda Loyalty Points'),
        224: Asset(224, 'AERGO', 'Aergo'),
        225: Asset(225, 'HARD', 'HARD Protocol'),
        226: Asset(226, 'FOR', 'ForTube'),
        227: Asset(227, 'SKL', 'SKALE Network'),
        228: Asset(228, 'DLT', 'Agrello'),
        229: Asset(229, 'OST', 'OST'),
        230: Asset(230, 'PSG', 'Paris Saint-Germain Fan Token'),
        231: Asset(231, 'JUV', 'Juventus Fan Token'),
        232: Asset(232, 'MTH', 'Monetha'),
        233: Asset(233, 'OAX', 'openANX'),
        234: Asset(234, 'EVX', 'Everex'),
        235: Asset(235, 'VIB', 'Viberate'),
        236: Asset(236, 'RDN', 'Raiden Network Token'),
        237: Asset(237, 'BCPT', 'BlockMason Credit Protocol'),
        238: Asset(238, 'CDT', 'Blox'),
        239: Asset(239, 'AMB', 'Ambrosus'),
        240: Asset(240, 'CMT', 'CyberMiles'),
        241: Asset(241, 'GO', 'GoChain'),
        242: Asset(242, 'CTXC', 'Cortex'),
        243: Asset(243, 'POA', 'POA Network'),
        244: Asset(244, 'ROSE', 'Oasis Network'),
        245: Asset(245, 'VIA', 'Viacoin'),
        246: Asset(246, 'SKY', 'Skycoin'),
        247: Asset(247, 'QKC', 'QuarkChain'),
        248: Asset(248, 'CTK', 'CertiK'),
        249: Asset(249, 'YOYO', 'YOYOW'),
        251: Asset(251, 'CELO', 'Celo'),
        252: Asset(252, 'COCOS', 'Cocos-BCX'),
        253: Asset(253, 'FIRO', 'Firo'),
        254: Asset(254, 'TWT', 'Trust Wallet Token'),
        255: Asset(255, 'TRU', 'TrueFi'),
        256: Asset(256, 'REEF', 'Reef Finance'),
        257: Asset(257, 'AXS', 'Axie Infinity'),
        258: Asset(258, 'BTCSTOLD', 'Bitcoin Standard Hashrate Token OLD'),
        259: Asset(259, 'SNMOLD', 'SONM Old'),
        260: Asset(260, 'APPC', 'AppCoins'),
        261: Asset(261, 'IDEX', 'IDEX'),
        262: Asset(262, 'UNFI', 'Unifi Protocol DAO'),
        263: Asset(263, 'DODO', 'DODO'),
        264: Asset(264, 'CAKE', 'PancakeSwap'),
        265: Asset(265, 'RIF', 'RSK Infrastructure Framework'),
        266: Asset(266, 'NBS', 'New BitShares'),
        268: Asset(268, 'FRONT', 'Frontier'),
        269: Asset(269, 'ACM', 'AC Milan Fan Token'),
        270: Asset(270, 'GXS', 'GXChain'),
        271: Asset(271, 'AUCTION', 'Auction'),
        272: Asset(272, 'BADGER', 'Badger DAO'),
        273: Asset(273, 'OM', 'MANTRA DAO'),
        274: Asset(274, 'LINA', 'Linear'),
        275: Asset(275, 'BTCST', 'Bitcoin Standard Hashrate Token'),
        276: Asset(276, 'DEGO', 'Dego Finance'),
        277: Asset(277, 'RAMP', 'RAMP'),
        278: Asset(278, 'PERP', 'Perpetual Protocol'),
        279: Asset(279, 'LIT', 'Litentry'),
        280: Asset(280, 'TVK', 'Terra Virtua'),
        281: Asset(281, 'FIS', 'Stafi'),
        282: Asset(282, 'PHA', 'Phala.Network'),
        283: Asset(283, 'ALICE', 'My Neighbor Alice'),
        284: Asset(284, 'DREP', 'DREP'),
        285: Asset(285, 'PUNDIX', 'Pundi X'),
        286: Asset(286, 'EPS', 'Ellipsis'),
        287: Asset(287, 'SUPER', 'SuperFarm'),
        288: Asset(288, 'AUTO', 'Auto'),
        289: Asset(289, 'ASR', 'AS Roma Fan Token'),
        290: Asset(290, 'GTO', 'Gifto'),
        291: Asset(291, 'CFX', 'Conflux Network'),
        292: Asset(292, 'SNM', 'SONM'),
        293: Asset(293, 'SHIB', 'SHIBA INU'),
        294: Asset(294, 'AGIX', 'SingularityNET Token'),
        295: Asset(295, 'SUN', 'SUN'),
        296: Asset(296, 'TORN', 'Tornado Cash'),
        297: Asset(297, 'GTC', 'Gitcoin'),
        298: Asset(298, 'MDX', 'Mdex'),
        299: Asset(299, 'MASK', 'Mask Network'),
        300: Asset(300, 'BAR', 'FC Barcelona Fan Token BAR'),
        301: Asset(301, 'MIR', 'Mirror Protocol'),
        302: Asset(302, 'TLM', 'Alien Worlds'),
        303: Asset(303, 'KEEP', 'Keep Network'),
        304: Asset(304, 'ERN', 'Ethernity Chain'),
        305: Asset(305, 'LPT', 'Livepeer'),
        306: Asset(306, 'QUICK', 'QuickSwap'),
        307: Asset(307, 'NU', 'NuCypher'),
        308: Asset(308, 'POLS', 'Polkastarter'),
        309: Asset(309, 'FORTH', 'Ampleforth Governance Token'),
        310: Asset(310, 'ICP', 'Internet Computer'),
        311: Asset(311, 'XYM', 'Symbol'),
        312: Asset(312, 'QNT', 'Quant'),
        313: Asset(313, 'FLOW', 'Flow'),
        315: Asset(315, 'CKB', 'CKB'),
        320: Asset(320, 'AR', 'Arweave'),
        321: Asset(321, 'SSV', 'SSV Token'),
        322: Asset(322, 'ILV', 'Illuvium'),
        323: Asset(323, 'RAY', 'Raydium'),
        324: Asset(324, 'DYDX', 'dYdX'),
        325: Asset(325, 'CLV', 'Clover Finance'),
        326: Asset(326, 'TRIBE', 'Tribe'),
        327: Asset(327, 'FARM', 'Harvest Finance'),
        328: Asset(328, 'BOND', 'BarnBridge'),
        329: Asset(329, 'BURGER', 'Burger Swap'),
        330: Asset(330, 'DEXE', 'DeXe'),
        331: Asset(331, 'MBOX', 'MOBOX'),
        332: Asset(332, 'SFP', 'SafePal'),
        333: Asset(333, 'SLP', 'Smooth Love Potion'),
        334: Asset(334, 'C98', 'Coin98'),
        335: Asset(335, 'YGG', 'Yield Guild Games'),
        336: Asset(336, 'MLN', 'Enzyme'),
        338: Asset(338, 'GALA', 'Gala'),
        339: Asset(339, 'GNO', 'Gnosis'),
        340: Asset(340, 'BAKE', 'BakeryToken'),
        341: Asset(341, 'AGLD', 'Adventure Gold'),
        342: Asset(342, 'TKO', 'Tokocrypto'),
        343: Asset(343, 'ALPACA', 'Alpaca Finance'),
        344: Asset(344, 'MINA', 'Mina'),
        345: Asset(345, 'MOVR', 'Moonriver'),
        346: Asset(346, 'GHST', 'Aavegotchi'),
        347: Asset(347, 'AMP', 'AMP'),
        348: Asset(348, 'OG', 'OG Fan Token'),
        349: Asset(349, 'PLA', 'PlayDapp'),
        350: Asset(350, 'PROM', 'Prometeus'),
        351: Asset(351, 'RAD', 'Radicle'),
        352: Asset(352, 'RARE', 'SuperRare'),
        353: Asset(353, 'PYR', 'Vulcan Forged PYR'),
        354: Asset(354, 'ATM', 'Atlético de Madrid Fan Token'),
        355: Asset(355, 'QI', 'BENQI'),
        356: Asset(356, 'FIDA', 'Bonfida'),
        357: Asset(357, 'ENS', 'Ethereum Name Service'),
        358: Asset(358, 'FXS', 'Frax Share'),
        359: Asset(359, 'JASMY', 'JasmyCoin'),
        360: Asset(360, 'LAZIO', 'Lazio Fan Token'),
        361: Asset(361, 'CITY', 'Manchester City Fan Token'),
        362: Asset(362, 'OOKI', 'OokiDAO'),
        363: Asset(363, 'SGB', 'Songbird'),
        364: Asset(364, 'BTTC', 'BitTorrent'),
        365: Asset(365, 'XNO', 'Nano token')
}