import { AssetPosition, AssetTrade } from './components/Positions';
import {TabsContainer} from './components/Tabs';
import {Trades} from './components/Trades';
import PriceGraphs from './components/PriceGraphs';
import ModelPerformance from './components/ModelPerformance';
import Settings from './components/Settings';
import React from 'react';
import ReactDOM from 'react-dom';

var next_timeout_id: NodeJS.Timeout;

export function main_loop(caller: string) {
	if(caller != 'timeout' && caller != 'init') {
		clearTimeout(next_timeout_id);
	}

	console.log('Render called');

	//Can just use a function to populate these arrays with data from the server
	var asset_position_array: {asset_id: string, asset_name: string, asset_count: number, aud_value: number, percentage_change: number}[] = [
		{
			asset_id: 'ETH',
			asset_name: 'Ethereum',
			asset_count: 2.002,
			aud_value: 10000.00,
			percentage_change: 10
		},
		{
			asset_id: 'BTC',
			asset_name: 'Bitcoin',
			asset_count: 0.05,
			aud_value: 3000.00,
			percentage_change: -2
		}
	]

	var asset_trade_array: {asset_id: string, asset_count: number, aud_value: number, timer: number}[] = [
		{
			asset_id: 'ETH', 
			asset_count: 2.002, 
			aud_value: 10000.00, 
			timer: 30
		}
	]

	//Render all
	ReactDOM.render(
		<React.StrictMode>
			<div className="column side_column" id="left_sidebar">
				<h2>StronkAI</h2>
				<hr className="title_separator" />
				<div className="positions_container" id="positions_container">
					{
						asset_position_array.length > 0 ?
							asset_position_array.map(({asset_id, asset_name, asset_count, aud_value, percentage_change}) => (
							<AssetPosition asset_id={asset_id} asset_name={asset_name} asset_count={asset_count} aud_value={aud_value} percentage_change={percentage_change} key={asset_id} />
							))
						: 
							<h3> No current positions </h3>
					}
				</div>
			</div>
			<div className="column centre_column" id="centre_column" style={{ borderLeftStyle: 'solid', borderWidth: '0.15em' }}>
				<div id="centre_tabs">
					<TabsContainer />
				</div>
			</div>
			<div className="column side_column" id="right_sidebar" style={{ borderLeftStyle: 'solid', borderWidth: '0.15em' }}>
				<h2>Upcoming trades</h2>
				<hr className="title_separator" />
				<div id="upcoming_trades_container">
					{
						asset_trade_array.length > 0 ?
							asset_trade_array.map(({asset_id, asset_count, aud_value, timer}) => (
							<AssetTrade asset_id={asset_id} asset_count={asset_count} aud_value={aud_value} timer={timer} key={asset_id} />
							)) 
						: 
							<h3> No upcoming trades </h3>
					}
				</div>
			</div>
		</React.StrictMode>,
		document.getElementById('root')
	);
	next_timeout_id = setTimeout(main_loop, 1000, 'timeout');
}