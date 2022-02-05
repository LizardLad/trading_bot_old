export {Asset};

class Asset {
	constructor(id, name) {
		this.id = id
		this.name = name

		this.position_template = `
<div class='position_container'>
    <div class='position_symbol position_column'>
        <em class='icon icon-${this.id}'></em>
    </div>
    <div class='position_left_col position_column'>
        <div class='position_asset_name position_element'>${this.id}</div>
        <div class='position_asset_amount position_element'>ASSET_COUNT</div>
    </div>
    <div class='position_right_col position_column'>
        <div class='position_aud_value position_element'>AUD_VALUE</div>
        <div class='position_percentage position_element'>PERCENTAGE_CHANGE</div>
    </div>
</div>
`;

		this.upcoming_trade_template = `
<div class='upcoming_trade_container'>
    <div class='upcoming_trade_symbol upcoming_trade_column'>
        <em class='icon icon-${this.id}'></em>
    </div>
    <div class='upcoming_trade_left_col upcoming_trade_column'>
        <div class='upcoming_trade_asset_name upcoming_trade_element'>${this.id}</div>
        <div class='upcoming_asset_amount upcoming_trade_element'>ASSET_COUNT</div>
    </div>
    <div class=upcoming_trade_right_col upcoming_trade_column'>
        <div class='upcoming_trade_aud_value position_element'>AUD_VALUE</div>
		<div class='upcoming_trade_timer position_element'>TIMER</div>
    </div>
</div>
`;
	}

	generate_asset_position() {
		//Need to fill in ASSET_COUNT, AUD_VALUE, and PERCENTAGE_CHANGE
		//For % change to be filled out the average buy price must be known
		//For ASSET_COUNT pull from server
		//For AUD_VALUE pull from server
		//For the moment though just return the template
		var html_string =  this.position_template;
		var container = document.getElementById('position_container');
		container.innerHTML = container.innerHTML + html_string;
	}

	generate_upcoming_trade(){
		//Need to fill in ASSET_COUNT, AUD_VALUE, and TIMER
		var html_string = this.upcoming_trade_template;
		var container = document.getElementById('upcoming_trades_container');
		container.innerHTML = container.innerHTML + html_string;
	}

}
