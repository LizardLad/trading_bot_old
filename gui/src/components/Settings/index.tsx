export { Settings };
import './settings.css';
import {format_number} from '../Positions';
import React, { useRef } from 'react';
import { make_request } from '../../utils/requests'

interface APIKeyInputProps {}
interface APIKeyInputState {
	modified: boolean;
	default: string;
}

class APIKeyInput extends React.Component<APIKeyInputProps, APIKeyInputState> {
	promise_list: any;
	__ismounted: boolean;
	constructor(props: APIKeyInputProps) {
		super(props);
		this.__ismounted = false;
		this.promise_list = [];
		this.state = {
			modified: false,
			default: 'api_key_default'
		}
		
		this.onChange = this.onChange.bind(this);
		this.update_default_value();
	}

	update_default_value() {
		const url = '/api/get/api_key';
		const request: { promise: Promise<any>; cancel(): void; } = make_request('GET', url, {});
		const id = Math.random();
		this.promise_list.push({...request, id: id});
		request.promise.then(
			async (response: string) => {
				const sleep = (ms: number) => new Promise(r => setTimeout(r, ms));
				while(this.__ismounted != true) {
					await sleep(1);
				}
				this.setState({default: response});
				//Remove promise from list
				for(var i = 0; i < this.promise_list.length; i++) {
					if(this.promise_list[i].id == id) {
						this.promise_list.splice(i, 1);
					}
				}
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

	onChange(e: React.ChangeEvent) {
		if(this.state.modified == false) {
			//Modified for the first time
			this.setState({modified: true})
		}
		let target = e.target as HTMLInputElement;
		this.setState({default: target.value});
	}

	render() {
		return (<>
			<p className='settings_label'>API Key Input:</p>
			<input type='text' name='api_key_input' className='text_input' onChange={this.onChange} value={this.state.default} />
		</>);
	}
}

interface TokenInputProps {}
interface TokenInputState {
	modified: boolean;
	default: string;
}

class TokenInput extends React.Component<TokenInputProps, TokenInputState> {
	promise_list: any = [];
	__ismounted: boolean;
	constructor(props: TokenInputProps) {
		super(props);
		this.promise_list = [];
		this.__ismounted = false;
		this.state = {
			modified: false,
			default: 'token_default'
		}
		
		this.onChange = this.onChange.bind(this);
		this.update_default_value();
	}

	update_default_value() {
		const url = '/api/get/token';
		const request: { promise: Promise<any>; cancel(): void; } = make_request('GET', url, {});
		const id = Math.random();
		this.promise_list.push({...request, id: id});
		request.promise.then(
			async (response: string) => {
				const sleep = (ms: number) => new Promise(r => setTimeout(r, ms));
				while(this.__ismounted != true) {
					await sleep(1);
				}
				this.setState({default: response});
				//Remove promise from list
				for(var i = 0; i < this.promise_list.length; i++) {
					if(this.promise_list[i].id == id) {
						this.promise_list.splice(i, 1);
					}
				}
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

	onChange(e: React.ChangeEvent) {
		if(this.state.modified == false) {
			//Modified for the first time
			this.setState({modified: true});
		}
		let target = e.target as HTMLInputElement;
		this.setState({default: target.value});
	}

	render() {
		return (<>
			<p className='settings_label'>Token Input:</p>
			<input type='text' name='token_input' className='text_input' onChange={this.onChange} value={this.state.default} />
		</>);
	}
}

interface ConfidenceInputProps {}
interface ConfidenceInputState {
	modified: boolean;
	default: number;
}

class ConfidenceInput extends React.Component<ConfidenceInputProps, ConfidenceInputState> {
	__ismounted: boolean;
	promise_list: { promise: Promise<any>; cancel: () => void; id: number}[] = [];
	constructor(props: ConfidenceInputProps) {
		super(props);
		this.__ismounted = false;
		this.promise_list = [];
		this.state = {
			modified: false,
			default: 0.00
		}
		
		this.onChange = this.onChange.bind(this);
		this.update_default_value();
	}

	update_default_value() {
		const url = '/api/get/confidence_threshold';
		const request: { promise: Promise<any>; cancel(): void; } = make_request('GET', url, {});
		const id = Math.random();
		this.promise_list.push({...request, id: id});
		request.promise.then(
			async (response: string) => {
				const sleep = (ms: number) => new Promise(r => setTimeout(r, ms));
				while(this.__ismounted != true) {
					await sleep(1);
				}
				this.setState({default: Number(response)});
				//Remove promise from list
				for(var i = 0; i < this.promise_list.length; i++) {
					if(this.promise_list[i].id == id) {
						this.promise_list.splice(i, 1);
					}
				}
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

	onChange(e: React.ChangeEvent) {
		if(this.state.modified == false) {
			//Modified for the first time
			this.setState({modified: true});
		}
		
		let target = e.target  as HTMLInputElement;

		/*if(target.type == 'number') {
			if()
		}*/

		var strings: string = target.value
		strings = strings.replace(/[^0-9.]/g, '').replace(/(\..*?)\..*/g, '$1');
		this.setState({default: Number(target.value)});
	}

	render() {
		return (<>
			<p className='settings_label'>Trade Confidence Input:</p>
			<p style={{margin: 0}}>{this.state.default}%</p>
			<input type='range' name='trade_confidence_input' className='range_input'
					min='0.01' max='100.00' step='0.01'
					onChange={this.onChange} value={this.state.default} />
			<input type='number' style={{width: '18px', border: 'none', padding: 0}} onChange={this.onChange} value={this.state.default}
			  step='0.01'/>
		</>);
	}
}

function Settings() {
	return (
		<div className='tab_content'>
			Settings such as API key, confidence level etc go here
			<br />
			<br />
			<APIKeyInput />
			<br />
			<TokenInput />
			<br />
			<ConfidenceInput />
			<br />
			<button onClick={(e: React.MouseEvent) => {save_information_to_server()}}>Submit</button>
		</div>
	);
}

function save_information_to_server() {
	return;
}