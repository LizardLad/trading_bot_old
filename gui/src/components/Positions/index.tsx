export {AssetPosition, AssetTrade};

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
