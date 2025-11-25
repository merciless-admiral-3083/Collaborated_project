import { PieChart, Pie, Cell } from "recharts";

export default function RiskGauge({ value }) {
  const data = [
    { name: "risk", value },
    { name: "rest", value: 1 - value }
  ];

  return (
    <div className="flex flex-col items-center">
      <PieChart width={220} height={220}>
        <Pie
          data={data}
          innerRadius={70}
          outerRadius={100}
          dataKey="value"
          startAngle={180}
          endAngle={0}
        >
          <Cell fill="#EF4444" />
          <Cell fill="#E5E7EB" />
        </Pie>
      </PieChart>
      <p className="text-xl font-bold mt-[-40px]">{(value * 100).toFixed(1)}%</p>
    </div>
  );
}
