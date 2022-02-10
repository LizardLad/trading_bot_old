export {AssetPosition, AssetTrade};
import React from 'react';

type AssetPositionProps = {
	id: string,
	name: string,
	asset_count: number,
	aud_value: number,
	percentage_change: number
}

function AssetPosition({id, name, asset_count, aud_value, percentage_change}: AssetPositionProps){
	return (
		<div className='position_container'>
			<div className='position_symbol position_column'>
				<em className={'icon icon-' + id}></em>
			</div>
			<div className='position_left_col position_column'>
				<div className='position_asset_name position_element'>{id}</div>
				<div className='position_asset_amount position_element'>{asset_count}</div>
			</div>
			<div className='position_right_col position_column'>
				<div className='position_aud_value position_element'>{aud_value}</div>
				<div className='position_percentage position_element'>{percentage_change}</div>
			</div>
		</div>
	);
}

type AssetTradeProps = {
	id: string,
	asset_count: number,
	aud_value: number,
	timer: number
}

function AssetTrade({id, asset_count, aud_value, timer}: AssetTradeProps) {
	return (
		<div className='upcoming_trade_container'>
			<div className='upcoming_trade_symbol upcoming_trade_column'>
				<em className='icon icon-${this.id}'></em>
			</div>
			<div className='upcoming_trade_left_col upcoming_trade_column'>
				<div className='upcoming_trade_asset_name upcoming_trade_element'>{id}</div>
				<div className='upcoming_asset_amount upcoming_trade_element'>{asset_count}</div>
			</div>
			<div className='upcoming_trade_right_col upcoming_trade_column'>
				<div className='upcoming_trade_aud_value position_element'>{aud_value}</div>
				<div className='upcoming_trade_timer position_element'>{timer}</div>
			</div>
		</div>
	);
}
