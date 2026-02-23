"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
  const router = useRouter();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccessMsg("");

    try {
      const res = await fetch("http://127.0.0.1:3000/api/register", {
        method: "POST",

        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Registration failed");
        setLoading(false);
        return;
      }

      setSuccessMsg("Registration successful! Redirecting to login...");
      setTimeout(() => router.push("/login"), 1500);

    } catch (err) {
      setError("Server error. Make sure backend is running.");
    }

    setLoading(false);
  };

  return (
    <div className="flex justify-center items-center min-h-screen">
      <form
        onSubmit={handleRegister}
        className="bg-gray-900 p-10 rounded-xl shadow-lg w-full max-w-md"
      >
        <h1 className="text-3xl font-bold text-center mb-8">Create Account</h1>

        {error && (
          <p className="text-red-400 text-center mb-4 text-sm">{error}</p>
        )}

        {successMsg && (
          <p className="text-green-400 text-center mb-4 text-sm">
            {successMsg}
          </p>
        )}

        {/* Name */}
        <label className="text-sm text-gray-300">Full Name</label>
        <input
          type="text"
          required
          className="w-full mt-1 mb-4 p-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500"
          value={formData.name}
          onChange={(e) =>
            setFormData({ ...formData, name: e.target.value })
          }
        />

        {/* Email */}
        <label className="text-sm text-gray-300">Email</label>
        <input
          type="email"
          required
          className="w-full mt-1 mb-4 p-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500"
          value={formData.email}
          onChange={(e) =>
            setFormData({ ...formData, email: e.target.value })
          }
        />

        {/* Password */}
        <label className="text-sm text-gray-300">Password</label>
        <input
          type="password"
          required
          className="w-full mt-1 mb-4 p-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500"
          value={formData.password}
          onChange={(e) =>
            setFormData({ ...formData, password: e.target.value })
          }
        />

        {/* Button */}
        <button
          type="submit"
          disabled={loading}
          className="w-full mt-4 bg-blue-600 hover:bg-blue-700 py-3 rounded-lg font-semibold disabled:opacity-50"
        >
          {loading ? "Creating account..." : "Register"}
        </button>

        <p className="text-center text-sm text-gray-400 mt-4">
          Already have an account?{" "}
          <a href="/login" className="text-blue-400 hover:underline">
            Login
          </a>
        </p>
      </form>
    </div>
  );
}

