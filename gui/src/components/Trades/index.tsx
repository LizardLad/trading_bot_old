export {Trades, get_historical_trades};
import {format_number} from '../Positions';

import './trades.css'

type TradesProps = {
	trades: {asset_id: string, asset_name: string, asset_count: number, buy_time: string, buy_aud_value: number, sell_time: string, sell_aud_value: number}[]
}

function Trades({trades}: TradesProps) {
	return (
		<div className='tab_content'>
			<div className='trade_tab_content'>
				{trades.length > 0 ?
					trades.map(({asset_id, asset_name, asset_count, buy_time, buy_aud_value, sell_time, sell_aud_value}) => (
					<HistoricalTrade asset_id={asset_id} asset_name={asset_name} asset_count={asset_count} buy_time={buy_time} buy_aud_value={buy_aud_value} sell_time={sell_time} sell_aud_value={sell_aud_value} key={asset_id} />
					))
				: 
					<h3> No historical trades. </h3>
				}
			</div>
		</div>
	);
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

function get_historical_trades() {
	var trade_history: {asset_id: string, asset_name: string, asset_count: number, buy_time: string, buy_aud_value: number, sell_time: string, sell_aud_value: number}[] = [
		{
			asset_id: 'ETH',
			asset_name: 'Ethereum',
			asset_count: 0.5, 
			buy_time: '2:00pm 01/01/2022', 
			buy_aud_value: 1500, 
			sell_time: '4:00pm 01/01/2022', 
			sell_aud_value: 1700
		}
	]
	return trade_history;
}