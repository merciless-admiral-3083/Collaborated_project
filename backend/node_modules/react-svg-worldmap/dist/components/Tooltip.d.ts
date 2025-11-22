import type { RefObject } from "react";
export interface Props {
    tip?: string;
    bgColor: string;
    textColor: string;
    pathRef: RefObject<SVGElement>;
    svgRef: RefObject<SVGSVGElement>;
}
export declare function Tooltip({ tip, ...props }: Props): JSX.Element | null;
export default Tooltip;
//# sourceMappingURL=Tooltip.d.ts.map