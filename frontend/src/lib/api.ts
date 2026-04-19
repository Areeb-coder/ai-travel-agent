export const API_BASE_URL = 
  process.env.NEXT_PUBLIC_BACKEND_URL?.replace(/\/+$/, "") || 
  "http://localhost:8000";

async function requestJson(path: string, init: RequestInit = {}) {
  const url = `${API_BASE_URL}${path.startsWith("/") ? path : `/${path}`}`;

  let res: Response;
  try {
    res = await fetch(url, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        ...(init.headers || {}),
      },
    });
  } catch (err) {
    // Network-level error: DNS, refused connection, CORS, etc.
    const reason =
      err instanceof Error ? err.message : JSON.stringify(err);
    throw new Error(
      `Failed to fetch ${url}: ${reason}. `
      + "Is the backend running and reachable from the browser?"
    );
  }

  let text = "";
  try {
    text = await res.text();
  } catch (e) {}

  if (!res.ok) {
    throw new Error(
      `Request to ${url} failed with status ${res.status}: ${text.slice(0, 500)}`
    );
  }

  try {
    return JSON.parse(text);
  } catch {
    return text as unknown;
  }
}

export async function postJson(path: string, body: unknown, init: RequestInit = {}) {
  return requestJson(path, {
    method: "POST",
    body: JSON.stringify(body),
    ...init,
  });
}
