"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";

import {
  FaEnvelope,
  FaLock,
  FaEye,
  FaEyeSlash,
} from "react-icons/fa";

import AuthLayout from "@/components/AuthLayout";
import Button from "@/components/Button";
import { COLORS } from "@/constants/theme";

export default function LoginPage() {
  const { login } = useAuth();
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);

  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const validate = () => {
    let valid = true;

    setEmailError("");
    setPasswordError("");

    if (!email.trim()) {
      setEmailError("Email is required");
      valid = false;
    } else if (email !== email.toLowerCase()) {
      setEmailError("Email should not contain uppercase letters");
      valid = false;
    } else if (email.includes(" ")) {
      setEmailError("Email should not contain spaces");
      valid = false;
    } else if (
      !/^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/.test(email)
    ) {
      setEmailError("Enter a valid email address");
      valid = false;
    }

    if (!password) {
      setPasswordError("Password is required");
      valid = false;
    } else if (password.length < 6) {
      setPasswordError("Password must be at least 6 characters");
      valid = false;
    }

    return valid;
  };

  const handleLogin = async () => {
    if (!validate()) return;

    setLoading(true);

    try {
      await login(email, password);

      // You can later use rememberMe for authentication logic
      console.log("Remember Me:", rememberMe);

      router.push("/dashboard");
    } catch (err) {
      setPasswordError(
        err instanceof Error ? err.message : "Login failed"
      );
    } finally {
      setLoading(false);
    }
  };
  return (
    <AuthLayout
      title="Welcome Back!"
      subtitle=""
    >
      <div className="space-y-5">

        {/* Email */}
        <div>
          <div className="relative">
            <FaEnvelope
              className="absolute left-4 top-4"
              style={{ color: COLORS.ocean }}
            />

            <input
              type="email"
              placeholder="Email Address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-lg py-3 pl-12 pr-4 border focus:outline-none focus:ring-2"
              style={{
                borderColor: COLORS.accent,
              }}
            />
          </div>

          {emailError && (
            <p className="text-red-500 text-sm mt-1">
              {emailError}
            </p>
          )}
        </div>

        {/* Password */}
        <div>
          <div className="relative">
            <FaLock
              className="absolute left-4 top-4"
              style={{ color: COLORS.ocean }}
            />

            <input
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-lg py-3 pl-12 pr-12 border focus:outline-none focus:ring-2"
              style={{
                borderColor: COLORS.accent,
              }}
            />

            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-4 top-4"
              style={{ color: COLORS.ocean }}
            >
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </button>
          </div>

          {passwordError && (
            <p className="text-red-500 text-sm mt-1">
              {passwordError}
            </p>
          )}
        </div>

        <div onClick={handleLogin}>
          <Button
            text="Login"
            loading={loading}
          />
        </div>

        <p
          className="text-center"
          style={{ color: COLORS.text }}
        >
          Don't have an account?{" "}
          <Link
            href="/register"
            className="font-semibold hover:underline"
            style={{ color: COLORS.ocean }}
          >
            Register
          </Link>
        </p>

      </div>
    </AuthLayout>
  );
}  