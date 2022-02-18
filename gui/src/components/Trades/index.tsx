export { Trades }; 
import React from 'react';
import { format_number } from '../Positions';
import { make_request } from '../../utils/requests'

import './trades.css';

interface TradesProps {}
interface TradesState {
	trades: {asset_id: string, asset_name: string, asset_count: number, buy_time: string, buy_aud_value: number, sell_time: string, sell_aud_value: number}[]
}

class Trades extends React.Component<TradesProps, TradesState> {
	__ismounted: boolean;
	promise_list: {promise: Promise<any>; cancel: () => void; id: number}[];
	prev_response: string;
	constructor(props: TradesProps) {
		super(props);
		this.__ismounted = false;
		this.promise_list = [];
		this.prev_response = '';
		this.state = {
			trades: []
		}
		this.update = this.update.bind(this);
		this.update();
	}

	update() {
		const url = '/api/get/trades';
		const request: { promise: Promise<any>; cancel(): void; } = make_request('GET', url, {});
		const id = Math.random();
		this.promise_list.push({...request, id: id});
		request.promise.then(
			async (response: string) => {
				const sleep = (ms: number) => new Promise(r => setTimeout(r, ms));
				while(this.__ismounted != true) {
					await sleep(1);
				}
				if(this.prev_response != response) {
					this.setState({trades: JSON.parse(response)});
					console.debug('Update trades object');
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

	render() {
		return (
			<div className='tab_content'>
			<div className='trade_tab_content'>
				{this.state.trades.length > 0 ?
					this.state.trades.map(({asset_id, asset_name, asset_count, buy_time, buy_aud_value, sell_time, sell_aud_value}) => (
					<HistoricalTrade asset_id={asset_id} asset_name={asset_name} asset_count={asset_count} buy_time={buy_time} buy_aud_value={buy_aud_value} sell_time={sell_time} sell_aud_value={sell_aud_value} key={asset_id} />
					))
				: 
					<h3> No historical trades. </h3>
				}
			</div>
		</div>
		);
	}
}

type HistoricalTradeProps = {
	asset_id: string,
	asset_name: string,
	asset_count: number, 
	buy_time: string, 
	buy_aud_value: number, 
	sell_time: string, 
	sell_aud_value: number
}

function HistoricalTrade({asset_id, asset_name, asset_count, buy_time, buy_aud_value, sell_time, sell_aud_value}: HistoricalTradeProps) {
	return (
		<>
			<em className={'icon icon-' + asset_id}></em> {asset_name} | {asset_count} {asset_id}
			<div className='trade_stats'> 
				| {buy_time} | ${format_number(buy_aud_value)} | {sell_time.length > 0 ? sell_time : 'Waiting...'} | {sell_aud_value > 0 ? '$'+format_number(sell_aud_value) : '-'} 
			</div>
			<hr className="trade_seperator" />
		</>
	);
}