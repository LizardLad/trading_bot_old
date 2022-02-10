import { AssetPosition, AssetTrade } from './positions';
import {TabBar} from './tabs';
import {Trades} from './trades';
import {PriceGraphs} from './price_graphs';
import {ModelPerformance} from './model_performance';
import {Settings} from './settings';
import React from 'react';
import ReactDOM from 'react-dom';

function main_init() {
	console.log('Hello from js');
	console.log('Create tabs');

	console.log('Do POST');
	const request = new XMLHttpRequest();
	const url = '/set/confidence_threshold'
	request.open('POST', url);
	request.setRequestHeader('Content-type', 'application/json')
	var data: object = {'key': 'value', 'deez': 'nutz'}
	var data_str: string = JSON.stringify(data)
	request.send(data_str);
	request.onreadystatechange=(e)=>{
		if(request.readyState === 4) {
			console.log(request);
		}
		else {;}
	}

	//Create ETH asset
	//var eth = new Asset('ETH', 'Ethereum');
	//eth.generate_asset_position();
	//eth.generate_upcoming_trade();

}

main_init();

interface TABS_INTERFACE {
	[key: string]: JSX.Element
}

const TABS: TABS_INTERFACE = {
	'trades': <Trades />,
	'price_graphs': <PriceGraphs />,
	'model_performance': <ModelPerformance />,
	'settings': <Settings />
}

export default function App() {
	const [selected_tab, set_selected_tab] = React.useState<string>('trades');

	const TabBar_properties = {
		set_selected_tab: set_selected_tab
	}

	return (
		<div>
			<TabBar {...TabBar_properties} />
			{TABS[selected_tab]}
		</div>
	);
}

ReactDOM.render(
	<App />,
	document.getElementById('centre_tabs')
);
  
