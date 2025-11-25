import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts";

export default function RiskTrendChart({ data }) {
  return (
    <LineChart width={500} height={250} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="time" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="risk" stroke="#3B82F6" strokeWidth={3} />
    </LineChart>
  );
}
