import { AssetPositions, AssetTrades } from './components/Positions';
import {TabsContainer} from './components/Tabs';
import {Trades} from './components/Trades';
import PriceGraphs from './components/PriceGraphs';
import ModelPerformance from './components/ModelPerformance';
import { Settings } from './components/Settings';
import React from 'react';
import ReactDOM from 'react-dom';

var next_timeout_id: NodeJS.Timeout;

export function main_loop(caller: string) {
	if(caller != 'timeout' && caller != 'init') {
		clearTimeout(next_timeout_id);
	}

	console.log('Render called');

	//Render all
	ReactDOM.render(
		<React.StrictMode>
			<div className="column side_column" id="left_sidebar">
				<h2>StronkAI</h2>
				<hr className="title_separator" />
				<div className="positions_container" id="positions_container">
					<AssetPositions />
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
					<AssetTrades />
				</div>
			</div>
		</React.StrictMode>,
		document.getElementById('root')
	);
	next_timeout_id = setTimeout(main_loop, 1000, 'timeout');
}