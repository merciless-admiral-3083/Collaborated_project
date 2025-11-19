import type { CSSProperties } from "react";
import type { SizeOption, CountryContext } from "./types.js";
export declare const defaultSize = "xl";
export declare const defaultColor = "#dddddd";
export declare const heightRatio: number;
export declare const sizeMap: Record<SizeOption, number>;
export declare const defaultCountryStyle: (stroke: string, strokeOpacity: number) => <T extends string | number>(context: CountryContext<T>) => CSSProperties;
export declare const defaultTooltip: <T extends string | number>(context: CountryContext<T>) => string;
//# sourceMappingURL=constants.d.ts.map