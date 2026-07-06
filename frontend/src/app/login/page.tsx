"use client";

import { useState } from "react";
import Link from "next/link";
import { FaEnvelope, FaLock, FaEye, FaEyeSlash } from "react-icons/fa";
import AuthLayout from "../../components/AuthLayout";
import Button from "../../components/Button";
import { COLORS } from "../../styles/colors";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  return (
    <AuthLayout
      title="Welcome Back!"
      subtitle="Login to continue managing your social media accounts."
    >
      <div className="space-y-5">
        {/* Email */}
        <div className="relative">
          <FaEnvelope className="absolute left-4 top-4 text-gray-400" />
          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border border-gray-300 rounded-lg py-3 pl-12 pr-4 focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
        </div>

        {/* Password */}
        <div className="relative">
          <FaLock className="absolute left-4 top-4 text-gray-400" />

          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border border-gray-300 rounded-lg py-3 pl-12 pr-12 focus:outline-none focus:ring-2 focus:ring-blue-600"
          />

          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-4 top-4 text-gray-500"
          >
            {showPassword ? <FaEyeSlash /> : <FaEye />}
          </button>
        </div>

        <Button text="Login" type="submit" />

        <p className="text-center" style={{ color: COLORS.text }}>
          Don't have an account?{" "}
          <Link
            href="/register"
            className="font-semibold"
            style={{ color: COLORS.secondary }}
          >
            Register
          </Link>
        </p>
      </div>
    </AuthLayout>
  );
}