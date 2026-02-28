"use client";
import { useEffect, useState } from "react";

export default function AdminPage() {

  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    fetch("http://localhost:8000/api/admin/analytics", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(res => res.json())
      .then(res => setData(res));
  }, []);

  if (!data) return <p>Loading...</p>;

  return (
    <div>
      <h1>Admin Dashboard</h1>

      <p>Total Users: {data.total_users}</p>
      <p>Total Predictions: {data.total_predictions}</p>
      <p>Last 7 Days Predictions: {data.predictions_last_7_days}</p>

      <h2>Risk Distribution</h2>
      {data.risk_distribution.map((item: any) => (
        <div key={item._id}>
          {item._id}: {item.count}
        </div>
      ))}

      <h2>Latest Retrain</h2>
      {data.latest_retrain && (
        <div>
          <p>Status: {data.latest_retrain.status}</p>
          <p>Version: {data.latest_retrain.model_version}</p>
        </div>
      )}
    </div>
  );
}