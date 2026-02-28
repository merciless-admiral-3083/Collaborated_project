"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function SummaryDashboard() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:3000/api/global-summary")
      .then(res => res.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return <p className="p-4">Loading...</p>;

  return (
    <div className="p-6 space-y-6">

      {/* Global Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader><CardTitle>Highest Risk Country</CardTitle></CardHeader>
          <CardContent className="text-2xl font-bold">{data.highest_risk.country}</CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>Lowest Risk Country</CardTitle></CardHeader>
          <CardContent className="text-2xl font-bold">{data.lowest_risk.country}</CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>Average Global Risk</CardTitle></CardHeader>
          <CardContent className="text-2xl font-bold">{data.average_risk}</CardContent>
        </Card>
      </div>

      {/* Country Risk Bar Chart */}
      <Card>
        <CardHeader><CardTitle>Country Risk Comparison</CardTitle></CardHeader>
        <CardContent style={{ height: 350 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data.risk_list}>
              <XAxis dataKey="country" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="risk_score" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
