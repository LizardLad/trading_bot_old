import './settings.css';

export default function Settings() {
	return (
		<div className='tab_content'>
			Settings such as API key, confidence level etc go here
			<br />
			<br />
			<p className='settings_label'>API Key Input:</p><input type='text' name='api_key_input' className='text_input'/>
			<br />
			<p className='settings_label'>Token Input:</p><input type='text' name='token_input' className='text_input'/>
			<br />
			<p className='settings_label'>Trade Confidence Input:</p><input type='text' name='trade_confidence_input' className='text_input'/>
		</div>
	);
}