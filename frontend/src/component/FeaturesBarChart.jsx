import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

export default function FeaturesBarChart({ data }) {
  return (
    <BarChart width={500} height={250} data={data}>
      <XAxis dataKey="feature" />
      <YAxis />
      <Tooltip />
      <Bar dataKey="impact" fill="#8B5CF6" />
    </BarChart>
  );
}
