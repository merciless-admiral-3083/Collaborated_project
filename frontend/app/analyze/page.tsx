"use client";

import { useState } from "react";

export default function RiskAnalyzerPage() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  const analyzeRisk = async () => {
    if (!input.trim()) {
      setError("Please enter details first.");
      return;
    }

    setError("");
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("http://localhost:3000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input }),
      });

      const data = await res.json();

      if (res.ok) {
        setResult(data);
      } else {
        setError(data.detail || "Something went wrong");
      }
    } catch (err) {
      setError("Unable to connect to backend.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen pb-20">
      
      {/* Title */}
      <h1 className="text-4xl font-bold mb-3">Risk Analyzer</h1>
      <p className="text-gray-400 mb-8">
        Enter supply chain details and get AI-generated risk insights.
      </p>

      {/* Input Box */}
      <textarea
        className="w-full h-40 p-4 rounded-xl bg-neutral-900 border border-neutral-700
        focus:outline-none focus:ring-2 focus:ring-blue-600"
        placeholder="Example: Supplier in Shenzhen reporting slower production due to power restrictions..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      {/* Button */}
      <button
        onClick={analyzeRisk}
        disabled={loading}
        className="mt-5 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800
        px-6 py-3 rounded-xl text-lg font-semibold transition"
      >
        {loading ? "Analyzing..." : "Analyze Risk"}
      </button>

      {/* Error */}
      {error && (
        <div className="mt-4 text-red-500 font-semibold">{error}</div>
      )}

      {/* Result */}
      {result && (
        <div className="mt-10 p-6 bg-neutral-900 rounded-2xl border border-neutral-800">

          <h2 className="text-2xl font-bold mb-4">
            🔍 Risk Analysis Result
          </h2>

          <div className="mb-6">
            <p className="text-gray-400 mb-2">Risk Score:</p>
            <p
              className={`text-4xl font-bold ${
                result.risk_score > 70
                  ? "text-red-500"
                  : result.risk_score > 40
                  ? "text-yellow-500"
                  : "text-green-500"
              }`}
            >
              {result.risk_score} / 100
            </p>
          </div>

          <div className="mt-4">
            <p className="text-gray-400 mb-2">AI Explanation:</p>
            <p className="text-gray-200 leading-relaxed">
              {result.explanation}
            </p>
          </div>

        </div>
      )}
    </div>
  );
}
