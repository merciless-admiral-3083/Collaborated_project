// lib/api.js
const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

async function parseResponse(res) {
  // Try to parse JSON; if it's HTML or not JSON, throw helpful error with text
  const text = await res.text();
  try {
    const json = JSON.parse(text);
    if (!res.ok) {
      const err = new Error(json?.message || "Request failed");
      err.status = res.status;
      err.payload = json;
      throw err;
    }
    return json;
  } catch (e) {
    // Not valid JSON — could be HTML error page
    const err = new Error(`Non-JSON response (status ${res.status}). Body starts with: ${text.slice(0, 200)}`);
    err.status = res.status;
    err.raw = text;
    throw err;
  }
}

export async function apiPost(path, body = {}, opts = {}) {
  const url = `${API.replace(/\/$/, "")}/${path.replace(/^\//, "")}`;
  const res = await fetch(url, {
    method: "POST",
    credentials: opts.credentials || "include",
    headers: {
      "Content-Type": "application/json",
      ...(opts.headers || {}),
    },
    body: JSON.stringify(body),
  });
  return parseResponse(res);
}
