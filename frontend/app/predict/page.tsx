"use client";
import { useState } from "react";

export default function PredictPage() {
  const [country, setCountry] = useState("");
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  async function callPredict() {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/predict", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ country, text })
      });
      const data = await res.json();
      setResult(data);
    } catch(err){
      console.error(err);
      alert("Prediction failed; check backend is running and CORS allowed.");
    }
    setLoading(false);
  }

  async function triggerTrain() {
    setLoading(true);
    try {
      // background training
      const res = await fetch("http://127.0.0.1:8000/api/train?background=true", { method: "POST" });
      const data = await res.json();
      alert("Training started: " + JSON.stringify(data));
    } catch(e) {
      alert("Start training failed");
    }
    setLoading(false);
  }

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Supply Chain Risk — Quick Predict</h1>

      <input className="border p-2 w-full mb-3" placeholder="Country (optional)" value={country} onChange={(e)=>setCountry(e.target.value)} />
      <textarea className="border p-2 w-full mb-3" rows={4} placeholder="Paste recent news / context..." value={text} onChange={(e)=>setText(e.target.value)} />

      <div className="flex gap-2">
        <button onClick={callPredict} disabled={loading} className="bg-blue-600 text-white px-4 py-2 rounded">Predict</button>
        <button onClick={triggerTrain} disabled={loading} className="bg-gray-600 text-white px-4 py-2 rounded">Start Training</button>
      </div>

      {result && (
        <div className="mt-6 p-4 border rounded">
          <h2 className="font-semibold">Result</h2>
          <p><b>Risk Score:</b> {result.risk_score}</p>
          <p><b>Status:</b> {result.status}</p>
        </div>
      )}
    </div>
  );
}
