export async function getGlobalSummary() {
  const res = await fetch("http://localhost:8000/api/global-summary");
  if (!res.ok) throw new Error("Failed to fetch summary");
  return res.json();
}
