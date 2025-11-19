"use client";

import { useState } from "react";

export default function RiskAnalyzer() {
  const [country, setCountry] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeRisk = async () => {
    if (!country.trim()) {
      setError("Please enter a country name.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ country }),
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError("Failed to connect to backend. Is FastAPI running?");
    }

    setLoading(false);
  };

  // Color coding risk status
  const riskColor = result?.status === "High risk"
    ? "text-red-600 font-semibold"
    : result?.status === "Moderate risk"
    ? "text-yellow-600 font-semibold"
    : "text-green-600 font-semibold";

  return (
    <div className="p-8 max-w-xl mx-auto bg-white rounded-2xl shadow-lg mt-10">
      <h1 className="text-2xl font-semibold mb-4 text-center">
        🌍 Global Risk Analyzer
      </h1>

      <input
        type="text"
        placeholder="Enter a country..."
        value={country}
        onChange={(e) => setCountry(e.target.value)}
        className="border px-3 py-2 w-full rounded-lg mb-4"
      />

      <button
        onClick={analyzeRisk}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 w-full"
      >
        {loading ? "Analyzing..." : "Analyze Risk"}
      </button>

      {error && (
        <p className="text-red-600 mt-4 text-center">{error}</p>
      )}

      {result && (
        <div className="mt-6 border-t pt-4 space-y-4">

          {/* Country + Risk Score */}
          <div>
            <p><strong>Country:</strong> {result.country}</p>
            <p><strong>Risk Score:</strong> {result.risk_score}</p>
            <p className={riskColor}>
              <strong>Status:</strong> {result.status}
            </p>
          </div>

          {/* Risk Factors */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="font-semibold mb-2">Top Risk Factors:</h3>
            {result.top_risk_factors?.length > 0 ? (
              <ul className="list-disc pl-5 space-y-1">
                {result.top_risk_factors.map((factor, i) => (
                  <li key={i}>{factor}</li>
                ))}
              </ul>
            ) : (
              <p>No major risk factors detected.</p>
            )}
          </div>

          {/* News Articles */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="font-semibold mb-2">Top Articles:</h3>
            {result.top_articles?.length > 0 ? (
              <ul className="space-y-2">
                {result.top_articles.map((a, i) => (
                  <li key={i} className="border-b pb-2">
                    <a
                      href={a.url || "#"}
                      target="_blank"
                      className="text-blue-600 font-medium hover:underline"
                    >
                      {a.title}
                    </a>
                    <p className="text-sm text-gray-600">{a.source}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No articles available.</p>
            )}
          </div>

        </div>
      )}
    </div>
  );
}
