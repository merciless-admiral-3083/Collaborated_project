"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.drawTooltip = void 0;
const tslib_1 = require("tslib");
const React = tslib_1.__importStar(require("react"));
const react_path_tooltip_1 = require("react-path-tooltip");
function drawTooltip(tip, tooltipBgColor, tooltipTextColor, rtl, triggerRef, containerRef) {
    return tip ? (React.createElement(react_path_tooltip_1.PathTooltip, { fontSize: 12, bgColor: tooltipBgColor, textColor: tooltipTextColor, key: tip, pathRef: triggerRef, svgRef: containerRef, rtl: rtl, tip: tip })) : null;
}
exports.drawTooltip = drawTooltip;
//# sourceMappingURL=draw.js.map