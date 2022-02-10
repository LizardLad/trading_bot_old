"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AssetTrade = exports.AssetPosition = void 0;
const react_1 = __importDefault(require("react"));
function AssetPosition({ id, name, asset_count, aud_value, percentage_change }) {
    return (react_1.default.createElement("div", { className: 'position_container' },
        react_1.default.createElement("div", { className: 'position_symbol position_column' },
            react_1.default.createElement("em", { className: 'icon icon-' + id })),
        react_1.default.createElement("div", { className: 'position_left_col position_column' },
            react_1.default.createElement("div", { className: 'position_asset_name position_element' }, id),
            react_1.default.createElement("div", { className: 'position_asset_amount position_element' }, asset_count)),
        react_1.default.createElement("div", { className: 'position_right_col position_column' },
            react_1.default.createElement("div", { className: 'position_aud_value position_element' }, aud_value),
            react_1.default.createElement("div", { className: 'position_percentage position_element' }, percentage_change))));
}
exports.AssetPosition = AssetPosition;
function AssetTrade({ id, asset_count, aud_value, timer }) {
    return (react_1.default.createElement("div", { className: 'upcoming_trade_container' },
        react_1.default.createElement("div", { className: 'upcoming_trade_symbol upcoming_trade_column' },
            react_1.default.createElement("em", { className: 'icon icon-${this.id}' })),
        react_1.default.createElement("div", { className: 'upcoming_trade_left_col upcoming_trade_column' },
            react_1.default.createElement("div", { className: 'upcoming_trade_asset_name upcoming_trade_element' }, id),
            react_1.default.createElement("div", { className: 'upcoming_asset_amount upcoming_trade_element' }, asset_count)),
        react_1.default.createElement("div", { className: 'upcoming_trade_right_col upcoming_trade_column' },
            react_1.default.createElement("div", { className: 'upcoming_trade_aud_value position_element' }, aud_value),
            react_1.default.createElement("div", { className: 'upcoming_trade_timer position_element' }, timer))));
}
exports.AssetTrade = AssetTrade;
