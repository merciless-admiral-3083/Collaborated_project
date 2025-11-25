const API = "http://localhost:8000/api";

export async function trainModel() {
  return fetch(`${API}/train`, { method: "POST" }).then(r => r.json());
}

export async function predictRisk(text) {
  return fetch(`${API}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  }).then(r => r.json());
}
