"use client";

import { useState } from "react";

export default function TrainPage() {
  const [loading, setLoading] = useState(false);
  const [metrics, setMetrics] = useState<any>(null);
  const [message, setMessage] = useState("");

  const startTraining = async () => {
    setLoading(true);
    setMessage("");
    setMetrics(null);

    try {
      const res = await fetch("http://127.0.0.1:3000/api/train", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });

      const data = await res.json();
      setLoading(false);

      if (data.status === "training_started_background") {
        setMessage("Training started in background ✔");
      } else {
        setMessage("Training completed ✔");
        setMetrics(data.metrics);
      }
    } catch (err) {
      setLoading(false);
      setMessage("Error starting training ❌");
    }
  };

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">ML Model Training Dashboard</h1>

      <p className="text-gray-600 mb-6">
        Click the button to retrain your Risk Prediction Model.
      </p>

      <button
        onClick={startTraining}
        disabled={loading}
        className={`px-6 py-3 rounded-md text-white ${
          loading ? "bg-gray-500" : "bg-blue-600 hover:bg-blue-700"
        }`}
      >
        {loading ? "Training..." : "Train Model"}
      </button>

      {message && (
        <p className="mt-6 text-lg font-medium">
          {message}
        </p>
      )}

      {metrics && (
        <div className="mt-6 p-4 border rounded-lg bg-gray-50">
          <h2 className="text-xl font-semibold mb-3">Training Metrics</h2>

          <pre className="p-3 bg-white rounded border overflow-x-auto">
            {JSON.stringify(metrics, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
