"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const tabs_1 = require("./tabs");
const trades_1 = require("./trades");
const price_graphs_1 = require("./price_graphs");
const model_performance_1 = require("./model_performance");
const settings_1 = require("./settings");
const react_1 = __importDefault(require("react"));
const react_dom_1 = __importDefault(require("react-dom"));
function main_init() {
    console.log('Hello from js');
    console.log('Create tabs');
    console.log('Do POST');
    const request = new XMLHttpRequest();
    const url = '/set/confidence_threshold';
    request.open('POST', url);
    request.setRequestHeader('Content-type', 'application/json');
    var data = { 'key': 'value', 'deez': 'nutz' };
    var data_str = JSON.stringify(data);
    request.send(data_str);
    request.onreadystatechange = (e) => {
        if (request.readyState === 4) {
            console.log(request);
        }
        else {
            ;
        }
    };
    //Create ETH asset
    //var eth = new Asset('ETH', 'Ethereum');
    //eth.generate_asset_position();
    //eth.generate_upcoming_trade();
}
main_init();
const TABS = {
    'trades': react_1.default.createElement(trades_1.Trades, null),
    'price_graphs': react_1.default.createElement(price_graphs_1.PriceGraphs, null),
    'model_performance': react_1.default.createElement(model_performance_1.ModelPerformance, null),
    'settings': react_1.default.createElement(settings_1.Settings, null)
};
function App() {
    const [selected_tab, set_selected_tab] = react_1.default.useState('trades');
    const TabBar_properties = {
        set_selected_tab: set_selected_tab
    };
    return (react_1.default.createElement("div", null,
        react_1.default.createElement(tabs_1.TabBar, Object.assign({}, TabBar_properties)),
        TABS[selected_tab]));
}
exports.default = App;
react_dom_1.default.render(react_1.default.createElement(App, null), document.getElementById('centre_tabs'));
