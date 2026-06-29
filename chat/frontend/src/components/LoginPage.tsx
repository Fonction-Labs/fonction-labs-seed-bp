import { useState } from "react";
import { login } from "../lib/auth";

interface Props {
  onSuccess: () => void;
}

export function LoginPage({ onSuccess }: Props) {
  const [password, setPassword] = useState("");
  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(false);
    const ok = await login(password);
    setLoading(false);
    if (ok) {
      onSuccess();
    } else {
      setError(true);
      setPassword("");
    }
  }

  return (
    <div className="flex h-screen w-screen items-center justify-center bg-gray-50">
      <div className="w-80 rounded-xl border border-gray-200 bg-white p-8 shadow-sm">
        <div className="mb-6 text-center">
          <h1 className="text-lg font-semibold text-gray-900">Fonction Labs</h1>
          <p className="mt-1 text-sm text-gray-500">Business Plan — Accès investisseurs</p>
        </div>
        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <input
            type="password"
            placeholder="Mot de passe"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoFocus
            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-500"
          />
          {error && (
            <p className="text-xs text-red-500">Mot de passe incorrect.</p>
          )}
          <button
            type="submit"
            disabled={loading || !password}
            className="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-50 hover:bg-gray-700 transition-colors"
          >
            {loading ? "Vérification…" : "Accéder →"}
          </button>
        </form>
      </div>
    </div>
  );
}
