"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid,
  ResponsiveContainer, BarChart, Bar
} from "recharts";

interface HistoryPoint {
  date: string;
  risk: number;
}

interface TopCountry {
  country: string;
  risk: number;
}

export default function DashboardPage() {
  const router = useRouter();

  const [history, setHistory] = useState<HistoryPoint[]>([]);
  const [top, setTop] = useState<TopCountry[]>([]);
  const [authorized, setAuthorized] = useState(false);

useEffect(() => {
  const token = localStorage.getItem("access_token");

  if (!token) {
    router.push("/login");
    return;
  }

  setAuthorized(true);

  // --- Global Summary ---
  fetch("http://localhost:8000/api/global_summary", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then(async (res) => {
      if (res.status === 401) {
        localStorage.removeItem("access_token");
        router.push("/login");
        return null;
      }
      return res.json();
    })
    .then((data) => {
      if (data?.country_risk_map) {
        const sorted = Object.entries(data.country_risk_map)
          .map(([country, risk]) => ({
            country,
            risk: Number(risk),
          }))
          .sort((a, b) => b.risk - a.risk)
          .slice(0, 8);

        setTop(sorted);
      }
    })
    .catch((err) => console.error("Error loading global summary:", err));

  // --- History ---
  fetch("http://localhost:8000/api/history/India?days=30", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then(async (res) => {
      if (res.status === 401) {
        localStorage.removeItem("access_token");
        router.push("/login");
        return null;
      }
      return res.json();
    })
    .then((data) => {
      if (Array.isArray(data)) {
        const formatted = data.reverse().map((d) => ({
          date: d.ts.split("T")[0],
          risk: d.risk_score,
        }));
        setHistory(formatted);
      }
    })
    .catch((err) => console.error("Error loading history:", err));
}, [router]);



if (!authorized) return null;
  return (
    <div className="pb-20">

      {/* PAGE TITLE */}
      <div className="mb-10">
        <h1 className="text-4xl font-bold">Dashboard</h1>
        <p className="text-gray-400 mt-1">
          Global supply chain risk monitoring
        </p>
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
          <h3 className="text-xl font-semibold mb-4">
            📉 30-Day Risk Trend (India)
          </h3>
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
          <h3 className="text-xl font-semibold mb-4">
            🔥 Top Countries (Highest Risk)
          </h3>
          <div className="w-full h-80">
            <ResponsiveContainer>
              <BarChart data={top}>
                <CartesianGrid strokeDasharray="3 3" stroke="#ddd" />
                <XAxis dataKey="country" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Bar
                  dataKey="risk"
                  fill="#ef4444"
                  radius={[6, 6, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}

/* ---- KPI TILE COMPONENT ---- */
function KpiTile(
  { label, value, color = "text-blue-600" }:
  { label: string; value: string; color?: string }
) {
  return (
    <div className="bg-white dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800 rounded-2xl p-5 shadow-sm hover:shadow-md transition">
      <div className="text-gray-500 text-sm">{label}</div>
      <div className={`text-2xl font-bold mt-1 ${color}`}>{value}</div>
    </div>
  );
}


