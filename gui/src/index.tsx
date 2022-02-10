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
    const url = '/set/confidence_threshold';
    request.open('POST', url);
    request.setRequestHeader('Content-type', 'application/json');
    var data: object = { key: 'value', deez: 'nutz' };
    var data_str: string = JSON.stringify(data);
    request.send(data_str);
    request.onreadystatechange = (e) => {
        if (request.readyState === 4) {
            console.log(request);
        } else {
        }
    };

    setInterval(main_loop, 1000);
    main_loop();
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

ReactDOM.render(
    <React.StrictMode>
        <div className="column side_column" id="left_sidebar">
            <h2>StronkAI</h2>
            <hr className="title_separator" />
            <div className="position_container" id="position_container">
                <div className="position_symbol position_column">
                    <em className="icon icon-ETH"></em>
                </div>
                <div className="position_left_col position_column">
                    <div className="position_asset_name position_element">
                        ETH
                    </div>
                    <div className="position_asset_amount position_element">
                        2.002
                    </div>
                </div>
                <div className="position_right_col position_column">
                    <div className="position_aud_value position_element">
                        10,000.00
                    </div>
                    <div className="position_percentage position_element">
                        +10%
                    </div>
                </div>
            </div>
            Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam
            nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat
            volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation
            ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo
            consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate
            velit esse molestie consequat, vel illum dolore eu feugiat nulla
            facilisis at vero eros et accumsan et iusto odio dignissim qui
            blandit praesent luptatum zzril delenit augue duis dolore te feugait
            nulla facilisi. Nam liber tempor cum soluta nobis eleifend option
            congue nihil imperdiet doming id quod mazim placerat facer possim
            assum.
        </div>
        <div className="column centre_column" id="centre_column" style={{ borderLeftStyle: 'solid', borderWidth: '0.15em' }}>
            <div id="centre_tabs"></div>
        </div>
        <div className="column side_column" id="right_sidebar" style={{ borderLeftStyle: 'solid', borderWidth: '0.15em' }}>
            <h2>Upcoming trades</h2>
            <hr className="title_separator" />
            <div id="upcoming_trades_container"></div>
            Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam
            nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat
            volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation
            ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo
            consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate
            velit esse molestie consequat, vel illum dolore eu feugiat nulla
            facilisis at vero eros et accumsan et iusto odio dignissim qui
            blandit praesent luptatum zzril delenit augue duis dolore te feugait
            nulla facilisi. Nam liber tempor cum soluta nobis eleifend option
            congue nihil imperdiet doming id quod mazim placerat facer possim
            assum.
        </div>
    </React.StrictMode>,
    document.getElementById('root')
);


let p = new Promise((resolve) => {
    ReactDOM.render(<App />, document.getElementById('centre_tabs'));
    resolve(true);
});
p.then(main_init);

