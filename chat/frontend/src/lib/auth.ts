const STORAGE_KEY = "bp_access_token";

export function getToken(): string | null {
  return localStorage.getItem(STORAGE_KEY);
}

export function isAuthenticated(): boolean {
  return !!getToken();
}

export async function login(password: string): Promise<boolean> {
  const expectedHash = import.meta.env.VITE_ACCESS_TOKEN_HASH as string;
  if (!expectedHash) {
    console.error("VITE_ACCESS_TOKEN_HASH not configured");
    return false;
  }
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
  if (hashHex === expectedHash.toLowerCase()) {
    localStorage.setItem(STORAGE_KEY, password);
    return true;
  }
  return false;
}

export function logout(): void {
  localStorage.removeItem(STORAGE_KEY);
}
