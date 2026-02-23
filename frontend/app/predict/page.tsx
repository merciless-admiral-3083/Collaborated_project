// "use client";
// import { useState } from "react";

// export default function PredictPage() {
//   const [country, setCountry] = useState("");
//   const [text, setText] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [result, setResult] = useState(null);

//   async function callPredict() {
//     setLoading(true);
//     try {
//       const res = await fetch("http://127.0.0.1:8000/api/predict", {
//         method: "POST",
//         headers: {"Content-Type":"application/json"},
//         body: JSON.stringify({ country, text })
//       });
//       const data = await res.json();
//       setResult(data);
//     } catch(err){
//       console.error(err);
//       alert("Prediction failed; check backend is running and CORS allowed.");
//     }
//     setLoading(false);
//   }

//   async function triggerTrain() {
//     setLoading(true);
//     try {
//       // background training
//       const res = await fetch("http://127.0.0.1:8000/api/train?background=true", { method: "POST" });
//       const data = await res.json();
//       alert("Training started: " + JSON.stringify(data));
//     } catch(e) {
//       alert("Start training failed");
//     }
//     setLoading(false);
//   }

//   return (
//     <div className="p-6 max-w-2xl mx-auto">
//       <h1 className="text-2xl font-bold mb-4">Supply Chain Risk — Quick Predict</h1>

//       <input className="border p-2 w-full mb-3" placeholder="Country (optional)" value={country} onChange={(e)=>setCountry(e.target.value)} />
//       <textarea className="border p-2 w-full mb-3" rows={4} placeholder="Paste recent news / context..." value={text} onChange={(e)=>setText(e.target.value)} />

//       <div className="flex gap-2">
//         <button onClick={callPredict} disabled={loading} className="bg-blue-600 text-white px-4 py-2 rounded">Predict</button>
//         <button onClick={triggerTrain} disabled={loading} className="bg-gray-600 text-white px-4 py-2 rounded">Start Training</button>
//       </div>

//       {result && (
//         <div className="mt-6 p-4 border rounded">
//           <h2 className="font-semibold">Result</h2>
//           <p><b>Risk Score:</b> {result.risk_score}</p>
//           <p><b>Status:</b> {result.status}</p>
//         </div>
//       )}
//     </div>
//   );
// }

"use client";

import { useState } from "react";

export default function PredictPage() {
  const [form, setForm] = useState({
    news_negative_pct: "",
    keyword_score: "",
    weather_risk: "",
    port_delay_index: "",
    supplier_concentration: "",
    hist_delay: "",
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<number | null>(null);
  const [error, setError] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handlePredict = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://localhost:3000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          features: [
            Number(form.news_negative_pct),
            Number(form.keyword_score),
            Number(form.weather_risk),
            Number(form.port_delay_index),
            Number(form.supplier_concentration),
            Number(form.hist_delay),
          ],
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data.prediction);
      } else {
        setError(data.detail || "Prediction error");
      }
    } catch (err) {
      setError("Server not reachable");
    }

    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto p-6">
      <h1 className="text-3xl font-semibold mb-6">Risk Prediction</h1>

      <div className="grid grid-cols-1 gap-4">
        {Object.keys(form).map((key) => (
          <div key={key}>
            <label className="block mb-1 font-medium">
              {key.replace(/_/g, " ").toUpperCase()}
            </label>
            <input
              type="number"
              name={key}
              value={form[key as keyof typeof form]}
              onChange={handleChange}
              className="border rounded-lg p-2 w-full"
            />
          </div>
        ))}
      </div>

      <button
        onClick={handlePredict}
        disabled={loading}
        className="mt-6 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
      >
        {loading ? "Predicting..." : "Predict"}
      </button>

      {result !== null && (
        <div className="mt-6 p-4 bg-green-100 text-green-700 rounded-lg">
          <p className="text-xl font-semibold">
            Predicted Risk Score: {result.toFixed(2)}
          </p>
        </div>
      )}

      {error && (
        <div className="mt-6 p-4 bg-red-100 text-red-700 rounded-lg">
          <p>Error: {error}</p>
        </div>
      )}
    </div>
  );
}
