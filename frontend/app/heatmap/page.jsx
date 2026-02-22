"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";

export default function RiskAnalyzer() {
  const searchParams = useSearchParams();
  const prefillCountry = searchParams.get("country");

  const [country, setCountry] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (prefillCountry) {
      setCountry(prefillCountry);
      analyzeRisk(prefillCountry);
    }
  }, [prefillCountry]);

  const analyzeRisk = async (inputCountry = country) => {
    if (!inputCountry) return;
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ country: inputCountry }),
      });

      setResult(await res.json());
    } catch (err) {
      console.error("Risk API error:", err);
    }

    setLoading(false);
  };

  return (
    <div className="pb-20 max-w-3xl mx-auto">

      {/* Title */}
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold">Risk Analyzer</h1>
        <p className="text-gray-500 mt-1">Search any country to detect supply chain risks</p>
      </div>

      {/* Search bar */}
      <div className="flex gap-3 sticky top-20 bg-gray-50 dark:bg-black py-4 z-20">
        <input
          type="text"
          placeholder="Enter a country..."
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          className="flex-1 px-4 py-3 rounded-xl border border-gray-300 dark:border-neutral-700 shadow-sm focus:ring-2 focus:ring-blue-500 outline-none text-lg"
        />

        <button
          onClick={() => analyzeRisk()}
          className="px-6 py-3 bg-blue-600 text-white rounded-xl shadow-md hover:bg-blue-700 transition w-40 text-lg"
        >
          Analyze
        </button>
      </div>

      {/* Loading */}
      {loading && (
        <p className="text-center mt-8 text-gray-400 animate-pulse text-lg">
          Analyzing risk...
        </p>
      )}

      {/* Results */}
      {result && !loading && (
        <div className="card mt-10 touch-pan-y">
          <h2 className="text-2xl font-bold mb-4">📊 Risk Report</h2>

          <div className="grid grid-cols-2 gap-4 mb-6">
            <Metric label="Risk Score" value={result.risk_score} color="text-red-500" />
            <Metric label="Risk Level" value={result.risk_label || "N/A"} color="text-blue-500" />
          </div>

          {/* Factors */}
          <h3 className="font-semibold text-lg mb-2">Top Risk Factors</h3>
          {result.top_risk_factors?.length ? (
            <ul className="list-disc ml-6 space-y-1 text-gray-700 dark:text-gray-300">
              {result.top_risk_factors.map((f, i) => <li key={i}>{f}</li>)}
            </ul>
          ) : (
            <p className="text-gray-500">No major risk factors identified.</p>
          )}

          {/* Explanation */}
          <h3 className="font-semibold text-lg mt-6 mb-1">Explanation</h3>
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
            {result.explanation ||
             "Based on recent news data, no critical supply-chain disruptions were detected."}
          </p>

          {/* Articles */}
          {result.top_articles?.length > 0 && (
            <>
              <h3 className="font-semibold text-lg mt-6 mb-3">📰 Related Articles</h3>
              <ul className="space-y-3">
                {result.top_articles.map((a, i) => (
                  <li key={i} className="p-4 rounded-xl bg-gray-100 dark:bg-neutral-800">
                    <a href={a.url} target="_blank" className="text-blue-600 underline text-lg">
                      {a.title}
                    </a>
                    <div className="text-sm text-gray-500">{a.source}</div>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}

/* ---- Metric Component ---- */
function Metric({ label, value, color }) {
  return (
    <div className="p-4 bg-gray-100 dark:bg-neutral-800 rounded-xl">
      <div className="text-gray-500 text-sm">{label}</div>
      <div className={`text-2xl font-bold mt-1 ${color}`}>{value}</div>
    </div>
  );
}
