"use client";

import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";

export default function TestPage() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    apiGet("/test")
      .then((res) => setData(res))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div style={{ padding: "30px" }}>
      <h1>Frontend → Backend Test</h1>

      {data && (
        <pre style={{ background: "#f5f5f5", padding: "20px" }}>
          {JSON.stringify(data, null, 2)}
        </pre>
      )}

      {error && <p style={{ color: "red" }}>Error: {error}</p>}
    </div>
  );
}


