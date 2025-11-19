"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";

export default function RiskAnalyzer() {
  const searchParams = useSearchParams();
  const prefillCountry = searchParams.get("country");

  const [country, setCountry] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Automatically run analysis if "?country=XYZ" exists
  useEffect(() => {
    if (prefillCountry) {
      setCountry(prefillCountry);
      analyzeRisk(prefillCountry);
    }
  }, [prefillCountry]);

  const analyzeRisk = async (c = country) => {
    if (!c) return;

    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ country: c }),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Error analyzing risk:", err);
    }

    setLoading(false);
  };

  return (
    <div className="p-10 max-w-3xl mx-auto">
      <h1 className="text-4xl font-bold text-center mb-6">
        Supply Chain Risk Analyzer
      </h1>

      <div className="flex gap-3 justify-center mb-6">
        <input
          type="text"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          placeholder="Enter a country..."
          className="border p-3 w-2/3 rounded-lg"
        />
        <button
          onClick={() => analyzeRisk()}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
        >
          Analyze
        </button>
      </div>

      {loading && (
        <p className="text-center text-gray-500 text-lg">Analyzing risk...</p>
      )}

      {result && (
        <div className="border p-6 rounded-lg mt-6 bg-gray-50 shadow">
          <h2 className="text-2xl font-semibold mb-3">Risk Report</h2>

          <p className="text-lg mb-2">
            <strong>📊 Risk Score:</strong> {result.risk_score}
          </p>

          <p className="text-lg mb-2">
            <strong>⚠ Risk Label:</strong> {result.risk_label}
          </p>

          <h3 className="text-xl font-bold mt-4 mb-2">Explanation</h3>
          <p className="text-gray-700 whitespace-pre-line">
            {result.explanation}
          </p>
        </div>
      )}
    </div>
  );
}
