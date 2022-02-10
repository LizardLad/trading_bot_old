export {TabBar};
import React = require("react");

function fix_selected_classes(e: React.MouseEvent) {
	var tab_links = document.getElementsByClassName('tab_link'); 
	for(var i = 0; i < tab_links.length; i++) {
		tab_links[i].className = tab_links[i].className.replace(" active", "");
	}
	const target = e.target as HTMLButtonElement;
	target.className += ' active';
}

function TabBar({set_selected_tab}: {set_selected_tab: React.Dispatch<React.SetStateAction<string>>;}) {
	return (
		<div className='tab_links'>
			<button className='tab_link' id='default_tab' onClick={(e: React.MouseEvent) => {fix_selected_classes(e);set_selected_tab('trades');}}>Trades</button>
			<button className='tab_link' onClick={(e: React.MouseEvent) => {fix_selected_classes(e);set_selected_tab('price_graphs');}}>Price Graphs</button>
			<button className='tab_link' onClick={(e: React.MouseEvent) => {fix_selected_classes(e);set_selected_tab('model_performance');}}>Model Performace</button>
			<button className='tab_link' onClick={(e: React.MouseEvent) => {fix_selected_classes(e);set_selected_tab('settings');}}>Settings</button>
		</div>
	);
}