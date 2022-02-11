import { AssetPosition, AssetTrade } from './components/Positions';
import TabBar from './components/Tabs';
import Trades from './components/Trades';
import PriceGraphs from './components/PriceGraphs';
import ModelPerformance from './components/ModelPerformance';
import Settings from './components/Settings';
import React from 'react';
import ReactDOM from 'react-dom';

import App from './index'

var next_timeout_id: NodeJS.Timeout;

export function main_loop(caller: string) {
	if(caller === 'timeout') {
		clearTimeout(next_timeout_id);
	}

	console.log('Render called');

	//Render all
	ReactDOM.render(
		<React.StrictMode>
			<div className="column side_column" id="left_sidebar">
				<h2>StronkAI</h2>
				<hr className="title_separator" />
				<div className="position_container" id="position_container">
					<AssetPosition asset_id={'ETH'} asset_name={'Ethereum'} asset_count={2.002} aud_value={10000.00} percentage_change={10} />
				</div>
				Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam
				nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat
				volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation
				ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo
				consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate
				velit esse molestie consequat, vel illum dolore eu feugiat nulla
				facilisis at vero eros et accumsan et iusto odio dignissim qui
				blandit praesent luptatum zzril delenit augue duis dolore te feugait
				nulla facilisi. Nam liber tempor cum soluta nobis eleifend option
				congue nihil imperdiet doming id quod mazim placerat facer possim
				assum.
			</div>
			<div className="column centre_column" id="centre_column" style={{ borderLeftStyle: 'solid', borderWidth: '0.15em' }}>
				<div id="centre_tabs">
					<App />
				</div>
			</div>
			<div className="column side_column" id="right_sidebar" style={{ borderLeftStyle: 'solid', borderWidth: '0.15em' }}>
				<h2>Upcoming trades</h2>
				<hr className="title_separator" />
				<div id="upcoming_trades_container">
					<AssetTrade asset_id={'ETH'} asset_count={2.002} aud_value={10000.00} timer={30}/>
				</div>
				Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam
				nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat
				volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation
				ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo
				consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate
				velit esse molestie consequat, vel illum dolore eu feugiat nulla
				facilisis at vero eros et accumsan et iusto odio dignissim qui
				blandit praesent luptatum zzril delenit augue duis dolore te feugait
				nulla facilisi. Nam liber tempor cum soluta nobis eleifend option
				congue nihil imperdiet doming id quod mazim placerat facer possim
				assum.
			</div>
		</React.StrictMode>,
		document.getElementById('root')
	);
	next_timeout_id = setTimeout(main_loop, 1000, 'timeout');
}