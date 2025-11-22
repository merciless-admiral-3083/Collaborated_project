import { useLayoutEffect } from "react";
import type { SizeOption } from "./types.js";
/**
 * This hook is like useLayoutEffect, but without the SSR warning
 * It seems hacky but it's used in many React libs (Redux, Formik...)
 * Also mentioned here: https://github.com/facebook/react/issues/16956
 * It is useful when you need to update a ref as soon as possible after a React
 * render (before `useEffect`)
 */
export declare const useIsomorphicLayoutEffect: typeof useLayoutEffect;
export declare function useWindowWidth(): number;
export declare function responsify(sizeOption: SizeOption | "responsive", windowWidth: number): number;
//# sourceMappingURL=utils.d.ts.map