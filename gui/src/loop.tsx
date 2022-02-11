import { AssetPosition, AssetTrade } from './components/Positions';
import TabBar from './components/Tabs';
import Trades from './components/Trades';
import PriceGraphs from './components/PriceGraphs';
import ModelPerformance from './components/ModelPerformance';
import Settings from './components/Settings';
import React from 'react';
import ReactDOM from 'react-dom';

var next_timeout_id: NodeJS.Timeout;

export function main_loop(caller: string) {
	if(caller === 'timeout') {
		clearTimeout(next_timeout_id);
	}
	//Create ETH asset
	ReactDOM.render(<AssetPosition asset_id={'ETH'} asset_name={'Ethereum'} asset_count={2.002} aud_value={10000.00} percentage_change={10} />, document.getElementById('position_container'));
    ReactDOM.render(<AssetTrade asset_id={'ETH'} asset_count={2.002} aud_value={10000.00} timer={30}/>, document.getElementById('upcoming_trades_container'));

	next_timeout_id = setTimeout(main_loop, 1000, 'timeout');
}