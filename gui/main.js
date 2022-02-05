window.main_init = main_init
window.open_tab = open_tab

import { Asset } from '/positions.js'

function main_init() {
	console.log('Hello from js');
	console.log('Create tabs');
	
	document.getElementById('default_tab').click();

	console.log('Do POST');
	const request = new XMLHttpRequest();
	const url = '/set/confidence_threshold'
	request.open('POST', url);
	request.setRequestHeader('Content-type', 'application/json')
	var data = {'key': 'value', 'deez': 'nutz'}
	data = JSON.stringify(data)
	request.send(data);
	request.onreadystatechange=(e)=>{
		if(request.readyState === 4) {
			console.log(request);
		}
		else {;}
	}

	//Create ETH asset
	var eth = new Asset('ETH', 'Ethereum');
	eth.generate_asset_position();
	eth.generate_upcoming_trade();
}

function open_tab(evt, id) {
	var tab_content, tab_links;
	tab_content = document.getElementsByClassName('tab_content');
	for(var i = 0; i < tab_content.length; i++) {
		tab_content[i].style.display = 'none';
	}
	tab_links = document.getElementsByClassName('tab_link');
	for(var i = 0; i < tab_links.length; i++) {
		tab_links[i].className = tab_links[i].className.replace(" active", "");
	}

	document.getElementById(id).style.display = 'block';
	evt.currentTarget.className += " active";
	return 0;
}
