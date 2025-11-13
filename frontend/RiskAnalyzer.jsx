import { useState } from "react";

export default function RiskAnalyzer() {
  const [country, setCountry] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeRisk = async () => {
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
    <div className="p-8 max-w-lg mx-auto bg-white rounded-2xl shadow-lg mt-10">
      <h1 className="text-2xl font-semibold mb-4 text-center">🌍 Global Risk Analyzer</h1>

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

      {result && (
        <div className="mt-6 border-t pt-4">
          <p><strong>Country:</strong> {result.country}</p>
          <p><strong>Risk Score:</strong> {result.risk_score}</p>
          <p><strong>Status:</strong> {result.status}</p>
        </div>
      )}
    </div>
  );
}
