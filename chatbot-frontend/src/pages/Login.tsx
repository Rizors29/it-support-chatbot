import { useState } from "react";
import { loginUser } from "../services/api";
import type { AuthUser } from "../types/chat";

interface LoginPageProps {
  onLogin: (user: AuthUser, token: string) => void;
}

function Login({ onLogin }: LoginPageProps) {
  const [email, setEmail] = useState("admin@finnet.co.id");
  const [password, setPassword] = useState("admin123");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async () => {
    if (!email || !password) {
      setError("Email dan password wajib diisi.");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const response = await loginUser({ email, password });

      localStorage.setItem("token", response.access_token);
      localStorage.setItem("user", JSON.stringify(response.user));

      onLogin(response.user, response.access_token);
    } catch {
      setError("Email atau password salah.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-100 px-4">
      <div className="w-full max-w-md rounded-3xl bg-white p-8 shadow-lg">
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-100">
            <img src="/chatbot-icon.svg" alt="Chatbot Icon" className="h-10 w-10" />
          </div>
          <h1 className="text-2xl font-bold text-slate-800">Login Chatbot</h1>
          <p className="mt-2 text-sm text-slate-500">
            Finnet IT Support Chatbot
          </p>
        </div>

        {error && (
          <div className="mb-4 rounded-xl bg-red-100 px-4 py-3 text-sm font-medium text-red-700">
            {error}
          </div>
        )}

        <div className="space-y-4">
          <div>
            <label className="mb-2 block text-sm font-semibold text-slate-700">
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500"
              placeholder="admin@finnet.co.id"
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-semibold text-slate-700">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") handleLogin();
              }}
              className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500"
              placeholder="Masukkan password"
            />
          </div>

          <button
            onClick={handleLogin}
            disabled={isLoading}
            className="w-full rounded-xl bg-blue-900 px-4 py-3 font-semibold text-white transition hover:bg-blue-950 disabled:opacity-60 cursor-pointer"
          >
            {isLoading ? "Memproses..." : "Login"}
          </button>
        </div>

        <div className="mt-6 rounded-xl bg-slate-50 p-4 text-sm text-slate-500">
          <p>
            <b>Admin:</b> admin@finnet.co.id / admin123
          </p>
          <p>
            <b>User:</b> user@finnet.co.id / user123
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;