"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.TabBar = void 0;
const react_1 = __importDefault(require("react"));
function fix_selected_classes(e) {
    var tab_links = document.getElementsByClassName('tab_link');
    for (var i = 0; i < tab_links.length; i++) {
        tab_links[i].className = tab_links[i].className.replace(" active", "");
    }
    const target = e.target;
    target.className += ' active';
}
function TabBar({ set_selected_tab }) {
    return (react_1.default.createElement("div", { className: 'tab_links' },
        react_1.default.createElement("button", { className: 'tab_link', id: 'default_tab', onClick: (e) => { fix_selected_classes(e); set_selected_tab('trades'); } }, "Trades"),
        react_1.default.createElement("button", { className: 'tab_link', onClick: (e) => { fix_selected_classes(e); set_selected_tab('price_graphs'); } }, "Price Graphs"),
        react_1.default.createElement("button", { className: 'tab_link', onClick: (e) => { fix_selected_classes(e); set_selected_tab('model_performance'); } }, "Model Performace"),
        react_1.default.createElement("button", { className: 'tab_link', onClick: (e) => { fix_selected_classes(e); set_selected_tab('settings'); } }, "Settings")));
}
exports.TabBar = TabBar;
