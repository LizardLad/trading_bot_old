import { AssetPosition, AssetTrade } from './components/Positions';
import TabBar from './components/Tabs';
import Trades from './components/Trades';
import PriceGraphs from './components/PriceGraphs';
import ModelPerformance from './components/ModelPerformance';
import Settings from './components/Settings';
import React from 'react';
import ReactDOM from 'react-dom';

import { main_loop } from './loop'

import '@assets/styles/base.css';
import '@assets/styles/icons.css';
import '@assets/styles/main.css';

function main_init() {
    console.log('Hello from js');
    console.log('Create tabs');

    document.getElementById('default_tab')?.click()

    console.log('Do POST');
    const request = new XMLHttpRequest();
    const url = '/api/set/confidence_threshold';
    request.open('POST', url);
    request.setRequestHeader('Content-type', 'application/json');
    var data: object = { key: 'value', deez: 'nutz' };
    var data_str: string = JSON.stringify(data);
    request.send(data_str);
    request.onreadystatechange = (e) => {
        if (request.readyState === 4) {
            console.log(request);
        }
    };
    main_loop('init');
}

interface TABS_INTERFACE {
    [key: string]: JSX.Element;
}

const TABS: TABS_INTERFACE = {
    trades: <Trades />,
    price_graphs: <PriceGraphs />,
    model_performance: <ModelPerformance />,
    settings: <Settings />,
};

export default function App() {
    const [selected_tab, set_selected_tab] = React.useState<string>('trades');

    const TabBar_properties = {
        set_selected_tab: set_selected_tab,
    };

    return (
        <div>
            <TabBar {...TabBar_properties} />
            {TABS[selected_tab]}
        </div>
    );
}


let p = new Promise((resolve) => {
    //ReactDOM.render(<App />, document.getElementById('centre_tabs'));
    resolve(true);
});
p.then(main_init);

