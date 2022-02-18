export {AssetPositions, AssetTrades, format_number, format_percentage};
import { make_request } from '../../utils/requests';
import React from 'react';
import './positions.css';

function format_number(num: number) {
	var value: string = Number(num).toFixed(2);
	var result: string = value.replace(/\B(?=(\d{3})+(?!\d))/g, ",");

	return result;
}

function format_percentage(num: number) {
	var result: string = format_number(num);

	if(num < 0) {
		result = '⮟' + result;
	}
	else {
		result = '⮝' + result;
	}

	return result;
}

function percentage_color(num: number) {
	var result: string;
	if(num < 0) {
		result = 'percentage_loss';
	}
	else {
		result = 'percentage_gain';
	}
	return result;
}

interface AssetPositionsProps {}
interface AssetPositionsState {
	modified: boolean;
	positions: {asset_id: string, asset_name: string, asset_count: number, aud_value: number, percentage_change: number}[];
}

class AssetPositions extends React.Component<AssetPositionsProps, AssetPositionsState> {
	__ismounted: boolean;
	promise_list: { promise: Promise<any>; cancel: () => void; id: number}[] = [];
	prev_response: string;
	constructor(props: AssetPositionsProps) {
		super(props);
		this.__ismounted = false;
		this.promise_list = [];
		this.state = {
			modified: false,
			positions: []
		}

		this.prev_response = '';
		
		this.update = this.update.bind(this);
		this.update();
	}

	update() {
		const url = '/api/get/positions';
		const request: { promise: Promise<any>; cancel(): void; } = make_request('GET', url, {});
		const id = Math.random();
		this.promise_list.push({...request, id: id});
		request.promise.then(
			async (response: string) => {
				const sleep = (ms: number) => new Promise(r => setTimeout(r, ms));
				while(this.__ismounted != true) {
					await sleep(1);
				}
				if(response != this.prev_response) {
					console.log(JSON.parse(response));
					this.setState({positions: JSON.parse(response)});
					this.prev_response = response;
				}
				//Remove promise from list
				for(var i = 0; i < this.promise_list.length; i++) {
					if(this.promise_list[i].id == id) {
						this.promise_list.splice(i, 1);
					}
				}
				setTimeout(this.update, 1000);
			}).catch((e: string) => {
				console.log(e);
			}
		);
	}

	componentDidMount() {
		this.__ismounted = true;
	}

	componentWillUnmount() {
		//Cancel all promises
		for(var i = 0; i < this.promise_list.length; i++)  {
			this.promise_list[i].cancel();
		}
		this.__ismounted = false;
	}

	render () {
		return (<>{this.state.positions.length > 0 ?
			this.state.positions.map(({asset_id, asset_name, asset_count, aud_value, percentage_change}) => (
			<AssetPosition asset_id={asset_id} asset_name={asset_name} asset_count={asset_count} aud_value={aud_value} percentage_change={percentage_change} key={asset_id} />
			))
		: 
			<h3> No current positions </h3>}</>);
	}
}

type AssetPositionProps = {
	asset_id: string,
	asset_name: string,
	asset_count: number,
	aud_value: number,
	percentage_change: number
}

function AssetPosition({asset_id, asset_name, asset_count, aud_value, percentage_change}: AssetPositionProps){
	return (
		<div className='position_container'>
			<div className='position_symbol position_column'>
				<em className={'icon icon-' + asset_id}></em>
			</div>
			<div className='position_left_col position_column'>
				<div className='position_asset_name position_element'>{asset_id}</div>
				<div className='position_asset_amount position_element'>{format_number(asset_count)}</div>
			</div>
			<div className='position_right_col position_column'>
				<div className='position_aud_value position_element'>{format_number(aud_value)}</div>
				<div className={'position_percentage position_element ' + percentage_color(percentage_change)}>{format_percentage(percentage_change)}</div>
			</div>
		</div>
	);
}

type AssetTradeProps = {
	asset_id: string,
	asset_count: number,
	aud_value: number,
	timer: number
}

function AssetTrade({asset_id, asset_count, aud_value, timer}: AssetTradeProps) {
	return (
		<div className='upcoming_trade_container'>
			<div className='upcoming_trade_symbol upcoming_trade_column'>
				<em className={'icon icon-'+asset_id}></em>
			</div>
			<div className='upcoming_trade_left_col upcoming_trade_column'>
				<div className='upcoming_trade_asset_name upcoming_trade_element'>{asset_id}</div>
				<div className='upcoming_asset_amount upcoming_trade_element'>{format_number(asset_count)}</div>
			</div>
			<div className='upcoming_trade_right_col upcoming_trade_column'>
				<div className='upcoming_trade_aud_value position_element'>{format_number(aud_value)}</div>
				<div className='upcoming_trade_timer position_element'>{timer}</div>
			</div>
			<div className='trade_decision_buttons'>
				<button className='trade_decision_button accept_button'>ACCEPT TRADE</button>
				<button className='trade_decision_button reject_button'>REJECT TRADE</button>
			</div>
		</div>
	);
}

interface AssetTradesProps {}
interface AssetTradesState {
	modified: boolean;
	trades: {asset_id: string, asset_count: number, aud_value: number, timer: number}[];
}

class AssetTrades extends React.Component<AssetTradesProps, AssetTradesState> {
	__ismounted: boolean;
	promise_list: { promise: Promise<any>; cancel: () => void; id: number}[] = [];
	prev_response = '';
	constructor(props: AssetPositionsProps) {
		super(props);
		this.__ismounted = false;
		this.promise_list = [];
		this.state = {
			modified: false,
			trades: []
		}
		
		this.prev_response = '';

		this.update = this.update.bind(this);
		this.update();
	}

	update() {
		const url = '/api/get/upcoming_trades';
		const request: { promise: Promise<any>; cancel(): void; } = make_request('GET', url, {});
		const id = Math.random();
		this.promise_list.push({...request, id: id});
		request.promise.then(
			async (response: string) => {
				const sleep = (ms: number) => new Promise(r => setTimeout(r, ms));
				while(this.__ismounted != true) {
					await sleep(1);
				}
				if(response != this.prev_response) {
					console.log(JSON.parse(response));
					this.setState({trades: JSON.parse(response)});
					this.prev_response = response;
				}
				//Remove promise from list
				for(var i = 0; i < this.promise_list.length; i++) {
					if(this.promise_list[i].id == id) {
						this.promise_list.splice(i, 1);
					}
				}
				setTimeout(this.update, 1000);
			}).catch((e: string) => {
				console.log(e);
			}
		);
	}

	componentDidMount() {
		this.__ismounted = true;
	}

	componentWillUnmount() {
		//Cancel all promises
		for(var i = 0; i < this.promise_list.length; i++)  {
			this.promise_list[i].cancel();
		}
		this.__ismounted = false;
	}

	render () {
		return (<>{
			this.state.trades.length > 0 ?
				this.state.trades.map(({asset_id, asset_count, aud_value, timer}) => (
				<AssetTrade asset_id={asset_id} asset_count={asset_count} aud_value={aud_value} timer={timer} key={asset_id} />
				)) 
			: 
				<h3> No upcoming trades </h3>
		}</>);
	}
}