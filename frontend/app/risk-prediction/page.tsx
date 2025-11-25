"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function RiskPredictionPage() {
  const [delay, setDelay] = useState("");
  const [inventory, setInventory] = useState("");
  const [transport, setTransport] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handlePredict = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          delay: parseFloat(delay),
          inventory: parseFloat(inventory),
          transport: parseFloat(transport),
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Error predicting risk.");
      } else {
        setResult(data);
      }
    } catch (e) {
      setError("Unable to reach backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-xl"
      >
        <Card className="shadow-lg p-6 rounded-2xl">
          <CardContent>
            <h1 className="text-2xl font-bold mb-4 text-center">
              Supply Chain Risk Prediction
            </h1>

            <div className="space-y-3">
              <div>
                <p className="mb-1">Delay (Days)</p>
                <Input
                  type="number"
                  value={delay}
                  onChange={(e) => setDelay(e.target.value)}
                  placeholder="Enter expected delay days"
                />
              </div>

              <div>
                <p className="mb-1">Inventory Level</p>
                <Input
                  type="number"
                  value={inventory}
                  onChange={(e) => setInventory(e.target.value)}
                  placeholder="Current inventory level"
                />
              </div>

              <div>
                <p className="mb-1">Transport Score</p>
                <Input
                  type="number"
                  value={transport}
                  onChange={(e) => setTransport(e.target.value)}
                  placeholder="Transport reliability score"
                />
              </div>

              <Button
                onClick={handlePredict}
                className="w-full mt-4 py-3 rounded-xl"
              >
                {loading ? "Predicting..." : "Predict Risk"}
              </Button>

              {error && (
                <p className="text-red-500 text-center mt-3">{error}</p>
              )}

              {result && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="mt-5 p-4 rounded-xl bg-green-100 border"
                >
                  <h2 className="text-lg font-semibold">Prediction Result</h2>
                  <p className="mt-1">
                    <strong>Risk Score:</strong> {result.risk_score}
                  </p>
                  <p>
                    <strong>Category:</strong> {result.risk_category}
                  </p>
                </motion.div>
              )}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
