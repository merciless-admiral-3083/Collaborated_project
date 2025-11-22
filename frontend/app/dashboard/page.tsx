"use client";

import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, BarChart, Bar } from "recharts";

export default function DashboardPage() {
  const [history, setHistory] = useState([]);
  const [top, setTop] = useState([]);

  useEffect(() => {
    // top countries from global_summary placeholder — adapt if you have real endpoint
    fetch("/api/global_summary")
      .then(r => r.json())
      .then(data => {
        // if server returns country_risk_map use it
        if(data.country_risk_map){
          const map = Object.entries(data.country_risk_map).map(([c, v]) => ({country: c, risk: v}));
          setTop(map.sort((a,b)=>b.risk-a.risk).slice(0,8));
        } else {
          setTop([{country:"IN", risk:45},{country:"US", risk:70},{country:"CN", risk:50}]);
        }
      });

    // example history for default country (India)
    fetch(`/api/history/India?days=30`).then(r => {
      if(r.ok) return r.json();
      return [];
    }).then(data => {
      setHistory(data.reverse().map(d => ({date: d.ts.split("T")[0], risk: d.risk_score})));
    }).catch(()=>{});
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card p-4">
          <h3 className="font-semibold mb-2">30-day Risk Trend (India)</h3>
          <div style={{ width: "100%", height: 300 }}>
            <ResponsiveContainer>
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Line type="monotone" dataKey="risk" stroke="#8884d8" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card p-4">
          <h3 className="font-semibold mb-2">Top countries (latest)</h3>
          <div style={{ width: "100%", height: 300 }}>
            <ResponsiveContainer>
              <BarChart data={top}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="country" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Bar dataKey="risk" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
