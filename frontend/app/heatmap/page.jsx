"use client";

import { useState } from "react";

export default function RiskAnalyzer() {
  const [country, setCountry] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeRisk = async () => {
    if (!country.trim()) return;

    setLoading(true);

    const res = await fetch("http://127.0.0.1:8000/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ country }),
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-center mb-8">
        Supply Chain Risk Analyzer
      </h1>

      <div className="flex gap-2">
        <input
          className="w-full border rounded-lg px-3 py-2"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          placeholder="India"
        />
        <button
          onClick={analyzeRisk}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg"
        >
          {loading ? "..." : "Analyze"}
        </button>
      </div>

      {result && (
  <div style={{ marginTop: "30px", padding: "20px", border: "1px solid #ddd", borderRadius: "10px" }}>
    <h2>Risk Report</h2>

    <p>📊 <b>Risk Score:</b> {result.risk_score}</p>
    <p>⚠ <b>Risk Label:</b> {result.status}</p>

    <hr />

    <h3>Top Risk Factors</h3>
    <ul>
      {result.top_risk_factors.length > 0 ? (
        result.top_risk_factors.map((f, i) => <li key={i}>{f}</li>)
      ) : (
        <p>No significant risk indicators found.</p>
      )}
    </ul>

    <h3>Explanation</h3>
    <p>
      {result.top_risk_factors.length > 0
        ? `Risks detected based on news keywords: ${result.top_risk_factors.join(", ")}.`
        : "News articles show no major known supply-chain risk indicators."}
    </p>
  </div>
)}


          {/* --- TOP ARTICLES --- */}
          {result.top_articles?.length > 0 && (
            <div className="mt-4">
              <h3 className="font-semibold">Top Articles:</h3>
              <ul className="space-y-2">
                {result.top_articles.map((a, i) => (
                  <li key={i}>
                    <a
                      href={a.url}
                      target="_blank"
                      className="text-blue-600 underline"
                    >
                      {a.title}
                    </a>
                    <div className="text-sm text-gray-600">{a.source}</div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
