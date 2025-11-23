"use client";

import { useEffect, useState } from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid,
  ResponsiveContainer, BarChart, Bar
} from "recharts";

export default function DashboardPage() {
  const [history, setHistory] = useState([]);
  const [top, setTop] = useState([]);

  useEffect(() => {
    fetch("/api/global_summary")
      .then(r => r.json())
      .then(data => {
        if (data.country_risk_map) {
          const sorted = Object.entries(data.country_risk_map)
            .map(([country, risk]) => ({ country, risk }))
            .sort((a, b) => b.risk - a.risk)
            .slice(0, 8);
          setTop(sorted);
        }
      });

    fetch(`/api/history/India?days=30`)
      .then(r => r.json())
      .then(data => {
        setHistory(
          data.reverse().map(d => ({
            date: d.ts.split("T")[0],
            risk: d.risk_score,
          }))
        );
      });
  }, []);

  return (
    <div className="pb-20">

      {/* PAGE TITLE */}
      <div className="mb-10">
        <h1 className="text-4xl font-bold">Dashboard</h1>
        <p className="text-gray-500 mt-1">Global supply chain risk monitoring</p>
      </div>

      {/* KPI TILES */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 mb-10">
        <KpiTile label="Countries Monitored" value="185+" />
        <KpiTile label="Daily Data Points" value="12,400+" />
        <KpiTile label="Active Alerts" value="17" color="text-red-500" />
        <KpiTile label="AI Model" value="v3.2" />
      </div>

      {/* GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">

        {/* LINE CHART */}
        <div className="card touch-pan-y">
          <h3 className="text-xl font-semibold mb-4">📉 30-Day Risk Trend (India)</h3>
          <div className="w-full h-80">
            <ResponsiveContainer>
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" stroke="#ddd" />
                <XAxis dataKey="date" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="risk"
                  stroke="#2563eb"
                  strokeWidth={3}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* BAR CHART */}
        <div className="card touch-pan-y">
          <h3 className="text-xl font-semibold mb-4">🔥 Top Countries (Highest Risk)</h3>
          <div className="w-full h-80">
            <ResponsiveContainer>
              <BarChart data={top}>
                <CartesianGrid strokeDasharray="3 3" stroke="#ddd" />
                <XAxis dataKey="country" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Bar dataKey="risk" fill="#ef4444" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ---- KPI TILE COMPONENT ---- */
function KpiTile({ label, value, color = "text-blue-600" }) {
  return (
    <div className="bg-white dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800 rounded-2xl p-5 shadow-sm hover:shadow-md transition cursor-default">
      <div className="text-gray-500 text-sm">{label}</div>
      <div className={`text-2xl font-bold mt-1 ${color}`}>{value}</div>
    </div>
  );
}
