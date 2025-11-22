"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Tooltip = void 0;
const tslib_1 = require("tslib");
const React = tslib_1.__importStar(require("react"));
const react_path_tooltip_1 = require("react-path-tooltip");
// TODO: need React.forwardRef to handle this
function Tooltip({ tip, ...props }) {
    return tip ? React.createElement(react_path_tooltip_1.PathTooltip, { fontSize: 12, tip: tip, ...props }) : null;
}
exports.Tooltip = Tooltip;
exports.default = Tooltip;
//# sourceMappingURL=Tooltip.js.map