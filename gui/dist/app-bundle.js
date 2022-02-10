/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./main.tsx":
/*!******************!*\
  !*** ./main.tsx ***!
  \******************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const positions_1 = __webpack_require__(/*! ./positions */ "./positions.tsx");
const tabs_1 = __webpack_require__(/*! ./tabs */ "./tabs.tsx");
const trades_1 = __webpack_require__(/*! ./trades */ "./trades.tsx");
const price_graphs_1 = __webpack_require__(/*! ./price_graphs */ "./price_graphs.tsx");
const model_performance_1 = __webpack_require__(/*! ./model_performance */ "./model_performance.tsx");
const settings_1 = __webpack_require__(/*! ./settings */ "./settings.tsx");
const react_1 = __importDefault(__webpack_require__(Object(function webpackMissingModule() { var e = new Error("Cannot find module 'react'"); e.code = 'MODULE_NOT_FOUND'; throw e; }())));
const react_dom_1 = __importDefault(__webpack_require__(Object(function webpackMissingModule() { var e = new Error("Cannot find module 'react-dom'"); e.code = 'MODULE_NOT_FOUND'; throw e; }())));
function main_init() {
    console.log('Hello from js');
    console.log('Create tabs');
    document.getElementById('default_tab').click();
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
    var eth = new positions_1.Asset('ETH', 'Ethereum');
    eth.generate_asset_position();
    eth.generate_upcoming_trade();
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
    return (react_1.default.createElement("div", null,
        react_1.default.createElement(tabs_1.TabBar, { set_selected_tab: set_selected_tab }),
        TABS[selected_tab]));
}
exports["default"] = App;
react_dom_1.default.render(react_1.default.createElement(App, null), document.getElementById('root'));


/***/ }),

/***/ "./model_performance.tsx":
/*!*******************************!*\
  !*** ./model_performance.tsx ***!
  \*******************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.ModelPerformance = void 0;
const React = __webpack_require__(Object(function webpackMissingModule() { var e = new Error("Cannot find module 'react'"); e.code = 'MODULE_NOT_FOUND'; throw e; }()));
function ModelPerformance() {
    return (React.createElement("div", { className: 'tab_content' }, "MODEL PERFORMANCE RIGHT HERE"));
}
exports.ModelPerformance = ModelPerformance;


/***/ }),

/***/ "./positions.tsx":
/*!***********************!*\
  !*** ./positions.tsx ***!
  \***********************/
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.Asset = void 0;
class Asset {
    constructor(id, name) {
        this.id = id;
        this.name = name;
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
        var html_string = this.position_template;
        var container = document.getElementById('position_container');
        container.innerHTML = container.innerHTML + html_string;
    }
    generate_upcoming_trade() {
        //Need to fill in ASSET_COUNT, AUD_VALUE, and TIMER
        var html_string = this.upcoming_trade_template;
        var container = document.getElementById('upcoming_trades_container');
        container.innerHTML = container.innerHTML + html_string;
    }
}
exports.Asset = Asset;


/***/ }),

/***/ "./price_graphs.tsx":
/*!**************************!*\
  !*** ./price_graphs.tsx ***!
  \**************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.PriceGraphs = void 0;
const React = __webpack_require__(Object(function webpackMissingModule() { var e = new Error("Cannot find module 'react'"); e.code = 'MODULE_NOT_FOUND'; throw e; }()));
function PriceGraphs() {
    return (React.createElement("div", { className: 'tab_content' }, "PRICE GRAPHS RIGHT HERE"));
}
exports.PriceGraphs = PriceGraphs;


/***/ }),

/***/ "./settings.tsx":
/*!**********************!*\
  !*** ./settings.tsx ***!
  \**********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.Settings = void 0;
const React = __webpack_require__(Object(function webpackMissingModule() { var e = new Error("Cannot find module 'react'"); e.code = 'MODULE_NOT_FOUND'; throw e; }()));
function Settings() {
    return (React.createElement("div", { className: 'tab_content' }, "SETTINGS RIGHT HERE"));
}
exports.Settings = Settings;


/***/ }),

/***/ "./tabs.tsx":
/*!******************!*\
  !*** ./tabs.tsx ***!
  \******************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.TabBar = void 0;
const React = __webpack_require__(Object(function webpackMissingModule() { var e = new Error("Cannot find module 'react'"); e.code = 'MODULE_NOT_FOUND'; throw e; }()));
function fix_selected_classes(e) {
    var tab_links = document.getElementsByClassName('tab_link');
    for (var i = 0; i < tab_links.length; i++) {
        tab_links[i].className = tab_links[i].className.replace(" active", "");
    }
    const target = e.target;
    target.className += ' active';
}
function TabBar(set_selected_tab) {
    return (React.createElement("div", { className: 'tab_links' },
        React.createElement("button", { className: 'tab_link', id: 'default_tab', onClick: (e) => { fix_selected_classes(e); set_selected_tab('trades'); } }, "Trades"),
        React.createElement("button", { className: 'tab_link', onClick: (e) => { fix_selected_classes(e); set_selected_tab('price_graphs'); } }, "Price Graphs"),
        React.createElement("button", { className: 'tab_link', onClick: (e) => { fix_selected_classes(e); set_selected_tab('model_performance'); } }, "Model Performace"),
        React.createElement("button", { className: 'tab_link', onClick: (e) => { fix_selected_classes(e); set_selected_tab('settings'); } }, "Settings")));
}
exports.TabBar = TabBar;


/***/ }),

/***/ "./trades.tsx":
/*!********************!*\
  !*** ./trades.tsx ***!
  \********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.Trades = void 0;
const React = __webpack_require__(Object(function webpackMissingModule() { var e = new Error("Cannot find module 'react'"); e.code = 'MODULE_NOT_FOUND'; throw e; }()));
function Trades() {
    return (React.createElement("div", { className: 'tab_content' }, "TRADES RIGHT HERE"));
}
exports.Trades = Trades;


/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module is referenced by other modules so it can't be inlined
/******/ 	var __webpack_exports__ = __webpack_require__("./main.tsx");
/******/ 	
/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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QUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7O1VBRUE7VUFDQTs7VUFFQTtVQUNBO1VBQ0E7Ozs7VUV0QkE7VUFDQTtVQUNBO1VBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9zdHJvbmthaS1ndWkvLi9tYWluLnRzeCIsIndlYnBhY2s6Ly9zdHJvbmthaS1ndWkvLi9tb2RlbF9wZXJmb3JtYW5jZS50c3giLCJ3ZWJwYWNrOi8vc3Ryb25rYWktZ3VpLy4vcG9zaXRpb25zLnRzeCIsIndlYnBhY2s6Ly9zdHJvbmthaS1ndWkvLi9wcmljZV9ncmFwaHMudHN4Iiwid2VicGFjazovL3N0cm9ua2FpLWd1aS8uL3NldHRpbmdzLnRzeCIsIndlYnBhY2s6Ly9zdHJvbmthaS1ndWkvLi90YWJzLnRzeCIsIndlYnBhY2s6Ly9zdHJvbmthaS1ndWkvLi90cmFkZXMudHN4Iiwid2VicGFjazovL3N0cm9ua2FpLWd1aS93ZWJwYWNrL2Jvb3RzdHJhcCIsIndlYnBhY2s6Ly9zdHJvbmthaS1ndWkvd2VicGFjay9iZWZvcmUtc3RhcnR1cCIsIndlYnBhY2s6Ly9zdHJvbmthaS1ndWkvd2VicGFjay9zdGFydHVwIiwid2VicGFjazovL3N0cm9ua2FpLWd1aS93ZWJwYWNrL2FmdGVyLXN0YXJ0dXAiXSwic291cmNlc0NvbnRlbnQiOlsiXCJ1c2Ugc3RyaWN0XCI7XG52YXIgX19pbXBvcnREZWZhdWx0ID0gKHRoaXMgJiYgdGhpcy5fX2ltcG9ydERlZmF1bHQpIHx8IGZ1bmN0aW9uIChtb2QpIHtcbiAgICByZXR1cm4gKG1vZCAmJiBtb2QuX19lc01vZHVsZSkgPyBtb2QgOiB7IFwiZGVmYXVsdFwiOiBtb2QgfTtcbn07XG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHsgdmFsdWU6IHRydWUgfSk7XG5jb25zdCBwb3NpdGlvbnNfMSA9IHJlcXVpcmUoXCIuL3Bvc2l0aW9uc1wiKTtcbmNvbnN0IHRhYnNfMSA9IHJlcXVpcmUoXCIuL3RhYnNcIik7XG5jb25zdCB0cmFkZXNfMSA9IHJlcXVpcmUoXCIuL3RyYWRlc1wiKTtcbmNvbnN0IHByaWNlX2dyYXBoc18xID0gcmVxdWlyZShcIi4vcHJpY2VfZ3JhcGhzXCIpO1xuY29uc3QgbW9kZWxfcGVyZm9ybWFuY2VfMSA9IHJlcXVpcmUoXCIuL21vZGVsX3BlcmZvcm1hbmNlXCIpO1xuY29uc3Qgc2V0dGluZ3NfMSA9IHJlcXVpcmUoXCIuL3NldHRpbmdzXCIpO1xuY29uc3QgcmVhY3RfMSA9IF9faW1wb3J0RGVmYXVsdChyZXF1aXJlKFwicmVhY3RcIikpO1xuY29uc3QgcmVhY3RfZG9tXzEgPSBfX2ltcG9ydERlZmF1bHQocmVxdWlyZShcInJlYWN0LWRvbVwiKSk7XG5mdW5jdGlvbiBtYWluX2luaXQoKSB7XG4gICAgY29uc29sZS5sb2coJ0hlbGxvIGZyb20ganMnKTtcbiAgICBjb25zb2xlLmxvZygnQ3JlYXRlIHRhYnMnKTtcbiAgICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnZGVmYXVsdF90YWInKS5jbGljaygpO1xuICAgIGNvbnNvbGUubG9nKCdEbyBQT1NUJyk7XG4gICAgY29uc3QgcmVxdWVzdCA9IG5ldyBYTUxIdHRwUmVxdWVzdCgpO1xuICAgIGNvbnN0IHVybCA9ICcvc2V0L2NvbmZpZGVuY2VfdGhyZXNob2xkJztcbiAgICByZXF1ZXN0Lm9wZW4oJ1BPU1QnLCB1cmwpO1xuICAgIHJlcXVlc3Quc2V0UmVxdWVzdEhlYWRlcignQ29udGVudC10eXBlJywgJ2FwcGxpY2F0aW9uL2pzb24nKTtcbiAgICB2YXIgZGF0YSA9IHsgJ2tleSc6ICd2YWx1ZScsICdkZWV6JzogJ251dHonIH07XG4gICAgdmFyIGRhdGFfc3RyID0gSlNPTi5zdHJpbmdpZnkoZGF0YSk7XG4gICAgcmVxdWVzdC5zZW5kKGRhdGFfc3RyKTtcbiAgICByZXF1ZXN0Lm9ucmVhZHlzdGF0ZWNoYW5nZSA9IChlKSA9PiB7XG4gICAgICAgIGlmIChyZXF1ZXN0LnJlYWR5U3RhdGUgPT09IDQpIHtcbiAgICAgICAgICAgIGNvbnNvbGUubG9nKHJlcXVlc3QpO1xuICAgICAgICB9XG4gICAgICAgIGVsc2Uge1xuICAgICAgICAgICAgO1xuICAgICAgICB9XG4gICAgfTtcbiAgICAvL0NyZWF0ZSBFVEggYXNzZXRcbiAgICB2YXIgZXRoID0gbmV3IHBvc2l0aW9uc18xLkFzc2V0KCdFVEgnLCAnRXRoZXJldW0nKTtcbiAgICBldGguZ2VuZXJhdGVfYXNzZXRfcG9zaXRpb24oKTtcbiAgICBldGguZ2VuZXJhdGVfdXBjb21pbmdfdHJhZGUoKTtcbn1cbm1haW5faW5pdCgpO1xuY29uc3QgVEFCUyA9IHtcbiAgICAndHJhZGVzJzogcmVhY3RfMS5kZWZhdWx0LmNyZWF0ZUVsZW1lbnQodHJhZGVzXzEuVHJhZGVzLCBudWxsKSxcbiAgICAncHJpY2VfZ3JhcGhzJzogcmVhY3RfMS5kZWZhdWx0LmNyZWF0ZUVsZW1lbnQocHJpY2VfZ3JhcGhzXzEuUHJpY2VHcmFwaHMsIG51bGwpLFxuICAgICdtb2RlbF9wZXJmb3JtYW5jZSc6IHJlYWN0XzEuZGVmYXVsdC5jcmVhdGVFbGVtZW50KG1vZGVsX3BlcmZvcm1hbmNlXzEuTW9kZWxQZXJmb3JtYW5jZSwgbnVsbCksXG4gICAgJ3NldHRpbmdzJzogcmVhY3RfMS5kZWZhdWx0LmNyZWF0ZUVsZW1lbnQoc2V0dGluZ3NfMS5TZXR0aW5ncywgbnVsbClcbn07XG5mdW5jdGlvbiBBcHAoKSB7XG4gICAgY29uc3QgW3NlbGVjdGVkX3RhYiwgc2V0X3NlbGVjdGVkX3RhYl0gPSByZWFjdF8xLmRlZmF1bHQudXNlU3RhdGUoJ3RyYWRlcycpO1xuICAgIHJldHVybiAocmVhY3RfMS5kZWZhdWx0LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIiwgbnVsbCxcbiAgICAgICAgcmVhY3RfMS5kZWZhdWx0LmNyZWF0ZUVsZW1lbnQodGFic18xLlRhYkJhciwgeyBzZXRfc2VsZWN0ZWRfdGFiOiBzZXRfc2VsZWN0ZWRfdGFiIH0pLFxuICAgICAgICBUQUJTW3NlbGVjdGVkX3RhYl0pKTtcbn1cbmV4cG9ydHMuZGVmYXVsdCA9IEFwcDtcbnJlYWN0X2RvbV8xLmRlZmF1bHQucmVuZGVyKHJlYWN0XzEuZGVmYXVsdC5jcmVhdGVFbGVtZW50KEFwcCwgbnVsbCksIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdyb290JykpO1xuIiwiXCJ1c2Ugc3RyaWN0XCI7XG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHsgdmFsdWU6IHRydWUgfSk7XG5leHBvcnRzLk1vZGVsUGVyZm9ybWFuY2UgPSB2b2lkIDA7XG5jb25zdCBSZWFjdCA9IHJlcXVpcmUoXCJyZWFjdFwiKTtcbmZ1bmN0aW9uIE1vZGVsUGVyZm9ybWFuY2UoKSB7XG4gICAgcmV0dXJuIChSZWFjdC5jcmVhdGVFbGVtZW50KFwiZGl2XCIsIHsgY2xhc3NOYW1lOiAndGFiX2NvbnRlbnQnIH0sIFwiTU9ERUwgUEVSRk9STUFOQ0UgUklHSFQgSEVSRVwiKSk7XG59XG5leHBvcnRzLk1vZGVsUGVyZm9ybWFuY2UgPSBNb2RlbFBlcmZvcm1hbmNlO1xuIiwiXCJ1c2Ugc3RyaWN0XCI7XG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHsgdmFsdWU6IHRydWUgfSk7XG5leHBvcnRzLkFzc2V0ID0gdm9pZCAwO1xuY2xhc3MgQXNzZXQge1xuICAgIGNvbnN0cnVjdG9yKGlkLCBuYW1lKSB7XG4gICAgICAgIHRoaXMuaWQgPSBpZDtcbiAgICAgICAgdGhpcy5uYW1lID0gbmFtZTtcbiAgICAgICAgdGhpcy5wb3NpdGlvbl90ZW1wbGF0ZSA9IGBcbjxkaXYgY2xhc3M9J3Bvc2l0aW9uX2NvbnRhaW5lcic+XG4gICAgPGRpdiBjbGFzcz0ncG9zaXRpb25fc3ltYm9sIHBvc2l0aW9uX2NvbHVtbic+XG4gICAgICAgIDxlbSBjbGFzcz0naWNvbiBpY29uLSR7dGhpcy5pZH0nPjwvZW0+XG4gICAgPC9kaXY+XG4gICAgPGRpdiBjbGFzcz0ncG9zaXRpb25fbGVmdF9jb2wgcG9zaXRpb25fY29sdW1uJz5cbiAgICAgICAgPGRpdiBjbGFzcz0ncG9zaXRpb25fYXNzZXRfbmFtZSBwb3NpdGlvbl9lbGVtZW50Jz4ke3RoaXMuaWR9PC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3M9J3Bvc2l0aW9uX2Fzc2V0X2Ftb3VudCBwb3NpdGlvbl9lbGVtZW50Jz5BU1NFVF9DT1VOVDwvZGl2PlxuICAgIDwvZGl2PlxuICAgIDxkaXYgY2xhc3M9J3Bvc2l0aW9uX3JpZ2h0X2NvbCBwb3NpdGlvbl9jb2x1bW4nPlxuICAgICAgICA8ZGl2IGNsYXNzPSdwb3NpdGlvbl9hdWRfdmFsdWUgcG9zaXRpb25fZWxlbWVudCc+QVVEX1ZBTFVFPC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3M9J3Bvc2l0aW9uX3BlcmNlbnRhZ2UgcG9zaXRpb25fZWxlbWVudCc+UEVSQ0VOVEFHRV9DSEFOR0U8L2Rpdj5cbiAgICA8L2Rpdj5cbjwvZGl2PlxuYDtcbiAgICAgICAgdGhpcy51cGNvbWluZ190cmFkZV90ZW1wbGF0ZSA9IGBcbjxkaXYgY2xhc3M9J3VwY29taW5nX3RyYWRlX2NvbnRhaW5lcic+XG4gICAgPGRpdiBjbGFzcz0ndXBjb21pbmdfdHJhZGVfc3ltYm9sIHVwY29taW5nX3RyYWRlX2NvbHVtbic+XG4gICAgICAgIDxlbSBjbGFzcz0naWNvbiBpY29uLSR7dGhpcy5pZH0nPjwvZW0+XG4gICAgPC9kaXY+XG4gICAgPGRpdiBjbGFzcz0ndXBjb21pbmdfdHJhZGVfbGVmdF9jb2wgdXBjb21pbmdfdHJhZGVfY29sdW1uJz5cbiAgICAgICAgPGRpdiBjbGFzcz0ndXBjb21pbmdfdHJhZGVfYXNzZXRfbmFtZSB1cGNvbWluZ190cmFkZV9lbGVtZW50Jz4ke3RoaXMuaWR9PC9kaXY+XG4gICAgICAgIDxkaXYgY2xhc3M9J3VwY29taW5nX2Fzc2V0X2Ftb3VudCB1cGNvbWluZ190cmFkZV9lbGVtZW50Jz5BU1NFVF9DT1VOVDwvZGl2PlxuICAgIDwvZGl2PlxuICAgIDxkaXYgY2xhc3M9dXBjb21pbmdfdHJhZGVfcmlnaHRfY29sIHVwY29taW5nX3RyYWRlX2NvbHVtbic+XG4gICAgICAgIDxkaXYgY2xhc3M9J3VwY29taW5nX3RyYWRlX2F1ZF92YWx1ZSBwb3NpdGlvbl9lbGVtZW50Jz5BVURfVkFMVUU8L2Rpdj5cblx0XHQ8ZGl2IGNsYXNzPSd1cGNvbWluZ190cmFkZV90aW1lciBwb3NpdGlvbl9lbGVtZW50Jz5USU1FUjwvZGl2PlxuICAgIDwvZGl2PlxuPC9kaXY+XG5gO1xuICAgIH1cbiAgICBnZW5lcmF0ZV9hc3NldF9wb3NpdGlvbigpIHtcbiAgICAgICAgLy9OZWVkIHRvIGZpbGwgaW4gQVNTRVRfQ09VTlQsIEFVRF9WQUxVRSwgYW5kIFBFUkNFTlRBR0VfQ0hBTkdFXG4gICAgICAgIC8vRm9yICUgY2hhbmdlIHRvIGJlIGZpbGxlZCBvdXQgdGhlIGF2ZXJhZ2UgYnV5IHByaWNlIG11c3QgYmUga25vd25cbiAgICAgICAgLy9Gb3IgQVNTRVRfQ09VTlQgcHVsbCBmcm9tIHNlcnZlclxuICAgICAgICAvL0ZvciBBVURfVkFMVUUgcHVsbCBmcm9tIHNlcnZlclxuICAgICAgICAvL0ZvciB0aGUgbW9tZW50IHRob3VnaCBqdXN0IHJldHVybiB0aGUgdGVtcGxhdGVcbiAgICAgICAgdmFyIGh0bWxfc3RyaW5nID0gdGhpcy5wb3NpdGlvbl90ZW1wbGF0ZTtcbiAgICAgICAgdmFyIGNvbnRhaW5lciA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdwb3NpdGlvbl9jb250YWluZXInKTtcbiAgICAgICAgY29udGFpbmVyLmlubmVySFRNTCA9IGNvbnRhaW5lci5pbm5lckhUTUwgKyBodG1sX3N0cmluZztcbiAgICB9XG4gICAgZ2VuZXJhdGVfdXBjb21pbmdfdHJhZGUoKSB7XG4gICAgICAgIC8vTmVlZCB0byBmaWxsIGluIEFTU0VUX0NPVU5ULCBBVURfVkFMVUUsIGFuZCBUSU1FUlxuICAgICAgICB2YXIgaHRtbF9zdHJpbmcgPSB0aGlzLnVwY29taW5nX3RyYWRlX3RlbXBsYXRlO1xuICAgICAgICB2YXIgY29udGFpbmVyID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3VwY29taW5nX3RyYWRlc19jb250YWluZXInKTtcbiAgICAgICAgY29udGFpbmVyLmlubmVySFRNTCA9IGNvbnRhaW5lci5pbm5lckhUTUwgKyBodG1sX3N0cmluZztcbiAgICB9XG59XG5leHBvcnRzLkFzc2V0ID0gQXNzZXQ7XG4iLCJcInVzZSBzdHJpY3RcIjtcbk9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBcIl9fZXNNb2R1bGVcIiwgeyB2YWx1ZTogdHJ1ZSB9KTtcbmV4cG9ydHMuUHJpY2VHcmFwaHMgPSB2b2lkIDA7XG5jb25zdCBSZWFjdCA9IHJlcXVpcmUoXCJyZWFjdFwiKTtcbmZ1bmN0aW9uIFByaWNlR3JhcGhzKCkge1xuICAgIHJldHVybiAoUmVhY3QuY3JlYXRlRWxlbWVudChcImRpdlwiLCB7IGNsYXNzTmFtZTogJ3RhYl9jb250ZW50JyB9LCBcIlBSSUNFIEdSQVBIUyBSSUdIVCBIRVJFXCIpKTtcbn1cbmV4cG9ydHMuUHJpY2VHcmFwaHMgPSBQcmljZUdyYXBocztcbiIsIlwidXNlIHN0cmljdFwiO1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7IHZhbHVlOiB0cnVlIH0pO1xuZXhwb3J0cy5TZXR0aW5ncyA9IHZvaWQgMDtcbmNvbnN0IFJlYWN0ID0gcmVxdWlyZShcInJlYWN0XCIpO1xuZnVuY3Rpb24gU2V0dGluZ3MoKSB7XG4gICAgcmV0dXJuIChSZWFjdC5jcmVhdGVFbGVtZW50KFwiZGl2XCIsIHsgY2xhc3NOYW1lOiAndGFiX2NvbnRlbnQnIH0sIFwiU0VUVElOR1MgUklHSFQgSEVSRVwiKSk7XG59XG5leHBvcnRzLlNldHRpbmdzID0gU2V0dGluZ3M7XG4iLCJcInVzZSBzdHJpY3RcIjtcbk9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBcIl9fZXNNb2R1bGVcIiwgeyB2YWx1ZTogdHJ1ZSB9KTtcbmV4cG9ydHMuVGFiQmFyID0gdm9pZCAwO1xuY29uc3QgUmVhY3QgPSByZXF1aXJlKFwicmVhY3RcIik7XG5mdW5jdGlvbiBmaXhfc2VsZWN0ZWRfY2xhc3NlcyhlKSB7XG4gICAgdmFyIHRhYl9saW5rcyA9IGRvY3VtZW50LmdldEVsZW1lbnRzQnlDbGFzc05hbWUoJ3RhYl9saW5rJyk7XG4gICAgZm9yICh2YXIgaSA9IDA7IGkgPCB0YWJfbGlua3MubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgdGFiX2xpbmtzW2ldLmNsYXNzTmFtZSA9IHRhYl9saW5rc1tpXS5jbGFzc05hbWUucmVwbGFjZShcIiBhY3RpdmVcIiwgXCJcIik7XG4gICAgfVxuICAgIGNvbnN0IHRhcmdldCA9IGUudGFyZ2V0O1xuICAgIHRhcmdldC5jbGFzc05hbWUgKz0gJyBhY3RpdmUnO1xufVxuZnVuY3Rpb24gVGFiQmFyKHNldF9zZWxlY3RlZF90YWIpIHtcbiAgICByZXR1cm4gKFJlYWN0LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIiwgeyBjbGFzc05hbWU6ICd0YWJfbGlua3MnIH0sXG4gICAgICAgIFJlYWN0LmNyZWF0ZUVsZW1lbnQoXCJidXR0b25cIiwgeyBjbGFzc05hbWU6ICd0YWJfbGluaycsIGlkOiAnZGVmYXVsdF90YWInLCBvbkNsaWNrOiAoZSkgPT4geyBmaXhfc2VsZWN0ZWRfY2xhc3NlcyhlKTsgc2V0X3NlbGVjdGVkX3RhYigndHJhZGVzJyk7IH0gfSwgXCJUcmFkZXNcIiksXG4gICAgICAgIFJlYWN0LmNyZWF0ZUVsZW1lbnQoXCJidXR0b25cIiwgeyBjbGFzc05hbWU6ICd0YWJfbGluaycsIG9uQ2xpY2s6IChlKSA9PiB7IGZpeF9zZWxlY3RlZF9jbGFzc2VzKGUpOyBzZXRfc2VsZWN0ZWRfdGFiKCdwcmljZV9ncmFwaHMnKTsgfSB9LCBcIlByaWNlIEdyYXBoc1wiKSxcbiAgICAgICAgUmVhY3QuY3JlYXRlRWxlbWVudChcImJ1dHRvblwiLCB7IGNsYXNzTmFtZTogJ3RhYl9saW5rJywgb25DbGljazogKGUpID0+IHsgZml4X3NlbGVjdGVkX2NsYXNzZXMoZSk7IHNldF9zZWxlY3RlZF90YWIoJ21vZGVsX3BlcmZvcm1hbmNlJyk7IH0gfSwgXCJNb2RlbCBQZXJmb3JtYWNlXCIpLFxuICAgICAgICBSZWFjdC5jcmVhdGVFbGVtZW50KFwiYnV0dG9uXCIsIHsgY2xhc3NOYW1lOiAndGFiX2xpbmsnLCBvbkNsaWNrOiAoZSkgPT4geyBmaXhfc2VsZWN0ZWRfY2xhc3NlcyhlKTsgc2V0X3NlbGVjdGVkX3RhYignc2V0dGluZ3MnKTsgfSB9LCBcIlNldHRpbmdzXCIpKSk7XG59XG5leHBvcnRzLlRhYkJhciA9IFRhYkJhcjtcbiIsIlwidXNlIHN0cmljdFwiO1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7IHZhbHVlOiB0cnVlIH0pO1xuZXhwb3J0cy5UcmFkZXMgPSB2b2lkIDA7XG5jb25zdCBSZWFjdCA9IHJlcXVpcmUoXCJyZWFjdFwiKTtcbmZ1bmN0aW9uIFRyYWRlcygpIHtcbiAgICByZXR1cm4gKFJlYWN0LmNyZWF0ZUVsZW1lbnQoXCJkaXZcIiwgeyBjbGFzc05hbWU6ICd0YWJfY29udGVudCcgfSwgXCJUUkFERVMgUklHSFQgSEVSRVwiKSk7XG59XG5leHBvcnRzLlRyYWRlcyA9IFRyYWRlcztcbiIsIi8vIFRoZSBtb2R1bGUgY2FjaGVcbnZhciBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX18gPSB7fTtcblxuLy8gVGhlIHJlcXVpcmUgZnVuY3Rpb25cbmZ1bmN0aW9uIF9fd2VicGFja19yZXF1aXJlX18obW9kdWxlSWQpIHtcblx0Ly8gQ2hlY2sgaWYgbW9kdWxlIGlzIGluIGNhY2hlXG5cdHZhciBjYWNoZWRNb2R1bGUgPSBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX19bbW9kdWxlSWRdO1xuXHRpZiAoY2FjaGVkTW9kdWxlICE9PSB1bmRlZmluZWQpIHtcblx0XHRyZXR1cm4gY2FjaGVkTW9kdWxlLmV4cG9ydHM7XG5cdH1cblx0Ly8gQ3JlYXRlIGEgbmV3IG1vZHVsZSAoYW5kIHB1dCBpdCBpbnRvIHRoZSBjYWNoZSlcblx0dmFyIG1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF0gPSB7XG5cdFx0Ly8gbm8gbW9kdWxlLmlkIG5lZWRlZFxuXHRcdC8vIG5vIG1vZHVsZS5sb2FkZWQgbmVlZGVkXG5cdFx0ZXhwb3J0czoge31cblx0fTtcblxuXHQvLyBFeGVjdXRlIHRoZSBtb2R1bGUgZnVuY3Rpb25cblx0X193ZWJwYWNrX21vZHVsZXNfX1ttb2R1bGVJZF0uY2FsbChtb2R1bGUuZXhwb3J0cywgbW9kdWxlLCBtb2R1bGUuZXhwb3J0cywgX193ZWJwYWNrX3JlcXVpcmVfXyk7XG5cblx0Ly8gUmV0dXJuIHRoZSBleHBvcnRzIG9mIHRoZSBtb2R1bGVcblx0cmV0dXJuIG1vZHVsZS5leHBvcnRzO1xufVxuXG4iLCIiLCIvLyBzdGFydHVwXG4vLyBMb2FkIGVudHJ5IG1vZHVsZSBhbmQgcmV0dXJuIGV4cG9ydHNcbi8vIFRoaXMgZW50cnkgbW9kdWxlIGlzIHJlZmVyZW5jZWQgYnkgb3RoZXIgbW9kdWxlcyBzbyBpdCBjYW4ndCBiZSBpbmxpbmVkXG52YXIgX193ZWJwYWNrX2V4cG9ydHNfXyA9IF9fd2VicGFja19yZXF1aXJlX18oXCIuL21haW4udHN4XCIpO1xuIiwiIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9