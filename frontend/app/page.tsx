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

  const analyzeRisk = async (c = country) => {
    if (!c) return;

    setLoading(true);

    try {
      const res = await fetch("http://localhost:3000/api/analyze", {
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
        <div
          style={{
            marginTop: "30px",
            padding: "20px",
            border: "1px solid #ddd",
            borderRadius: "10px",
          }}
        >
          <h2>Risk Report</h2>

          <p>
            📊 <b>Risk Score:</b> {result.risk_score}
          </p>
          <p>
            ⚠ <b>Risk Label:</b>{" "}
            {result.risk_label || result.status || "Unavailable"}
          </p>

          <hr />

          <h3>Top Risk Factors</h3>
          <ul>
            {result.top_risk_factors?.length > 0 ? (
              result.top_risk_factors.map((f, i) => <li key={i}>{f}</li>)
            ) : (
              <p>No significant risk indicators found.</p>
            )}
          </ul>

          <h3>Explanation</h3>
          <p>
            {result.explanation
              ? result.explanation
              : result.top_risk_factors?.length > 0
              ? `These factors were detected in recent news for ${
                  result.country || ""
                }.`
              : "No major supply chain risks detected based on current news."}
          </p>

          {result.top_articles?.length > 0 && (
            <>
              <h3 style={{ marginTop: 12 }}>Top Articles</h3>
              <ul>
                {result.top_articles.map((a, i) => (
                  <li key={i}>
                    <a
                      href={a.url || "#"}
                      target="_blank"
                      rel="noreferrer"
                      className="text-blue-600 underline"
                    >
                      {a.title || "(no title)"}
                    </a>
                    <div className="text-sm text-gray-600">{a.source}</div>
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
