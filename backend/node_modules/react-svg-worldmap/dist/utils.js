"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.responsify = exports.useWindowWidth = exports.useIsomorphicLayoutEffect = void 0;
const react_1 = require("react");
const constants_js_1 = require("./constants.js");
/**
 * This hook is like useLayoutEffect, but without the SSR warning
 * It seems hacky but it's used in many React libs (Redux, Formik...)
 * Also mentioned here: https://github.com/facebook/react/issues/16956
 * It is useful when you need to update a ref as soon as possible after a React
 * render (before `useEffect`)
 */
exports.useIsomorphicLayoutEffect = typeof window !== "undefined" ? react_1.useLayoutEffect : react_1.useEffect;
// Calculate window width
function useWindowWidth() {
    const [width, setWidth] = (0, react_1.useState)(constants_js_1.sizeMap[constants_js_1.defaultSize]);
    (0, exports.useIsomorphicLayoutEffect)(() => {
        const updateWidth = () => {
            setWidth(window.innerWidth);
        };
        window.addEventListener("resize", updateWidth);
        updateWidth();
        return () => window.removeEventListener("resize", updateWidth);
    }, []);
    return width;
}
exports.useWindowWidth = useWindowWidth;
// Adjust responsive size
function responsify(sizeOption, windowWidth) {
    if (sizeOption === "responsive") {
        // Make component work in SSR
        if (typeof window === "undefined")
            return constants_js_1.sizeMap[constants_js_1.defaultSize];
        return Math.min(window.innerHeight, window.innerWidth) * 0.75;
    }
    if (typeof window === "undefined")
        return constants_js_1.sizeMap[sizeOption];
    // First size that fits window size
    const fittingSize = Object.values(constants_js_1.sizeMap)
        .reverse()
        .find((size) => size <= windowWidth) ?? constants_js_1.sizeMap.sm;
    return Math.min(fittingSize, constants_js_1.sizeMap[sizeOption]);
}
exports.responsify = responsify;
//# sourceMappingURL=utils.js.map